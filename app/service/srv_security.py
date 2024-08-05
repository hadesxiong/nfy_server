# coding=utf8
import base64,jwt
from datetime import datetime,timedelta,timezone

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException, status

from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

from typing import Annotated

from tortoise.models import Model

from app.core.config import settings
from app.models.common import UserAuth
from app.api.controller.ctrl_error import CustomHTTPException


# 密码解密用于前后端交互时验证的密码
def decrypt_aes(
        encrypted_data:str,
        key:bytes,iv:bytes) -> str:
    
    try:
        # 将 Base64 编码的加密数据解码为字节串
        encrypted_bytes = base64.b64decode(encrypted_data)
        # 初始化 AES 解密器
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        # 解密数据
        decrypted_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
        # 去除填充
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        # 将解密后的字节串转换为字符串
        decrypted_text = unpadded_data.decode('utf-8')
        
        return decrypted_text

    except (ValueError, UnicodeError) as e:

        raise CustomHTTPException(status_code=123,detail=str(e))
    

# 加密解密功能初始化
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 获取密码hash
def get_pwd_hash(pwd:str,salt:str=None):
    return pwd_context.hash(pwd)

# 验证密码hash
def verify_pwd(plain_pwd:str,hashed_pwd:str):
    return pwd_context.verify(plain_pwd,hashed_pwd)

# 查询用户
def get_user(usr_model:Model,username:str):
    
    try:
        usr_ins = usr_model.filter(usr_name=username)
        if len(usr_ins) > 1:
            return False
        else:
            return usr_ins
    
    except:
        return False
    
# 校验用户
def auth_usr(usr_model:Model,username:str,password:str):

    user = get_user(usr_model,username)

    if not user:
        return False
    
    if not verify_pwd(password,user.usr_pwd):
        return False
    
    return user

# 创建token
def create_actoken(
        data:dict,
        expires_delta: timedelta | None = None):
    
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=2)
    
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encode_jwt

# 获取当前用户
async def get_current_user(
        # token: Annotated[str,Depends(oauth2_scheme)],
        token: str):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,  # 确保这里使用的是正确的密钥
            algorithms=[settings.ALGORITHM]  # 确保这里使用的是正确的算法列表
        )
        username: str = payload.get('username')
        if not username:
            raise credentials_exception
        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise credentials_exception
    
    # user = get_user(usr_model,user_name=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user

# 获取当前激活用户
async def get_current_active_user(
        current_user:Annotated[UserAuth,Depends(get_current_user)]):
    
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
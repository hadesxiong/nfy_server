# coding=utf8
from fastapi import APIRouter,Depends, Form

from app.api.schema.sch_user import UserInfoRes,UserAuthRes,UserInfoQuery
from app.api.controller.ctrl_user import *

from app.service.srv_security import decrypt_aes,get_current_user
from app.core.config import settings

# 定义路由
user_rt = APIRouter(
    prefix='/user',
    tags=['User','Basic Service'],
)

# 获取用户信息
@user_rt.get(
        '/getUserInfo',
        response_model=UserInfoRes,
        response_model_exclude_unset=True)

async def getUser(
        params: UserInfoQuery = Depends(),
        current_user: str = Depends(get_current_user)):
        
        # 清理查询参数
        fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
        
        rslt = await get_userinfo_handler(fltr_pars)

        return UserInfoRes(
            code = 200,
            msg = 'success',
            data = rslt.items,
            has_next = rslt.page < rslt.pages
        )

# 用户注册
@user_rt.post(
        '/userRegister',
        response_model=UserAuthRes,
        response_model_exclude_unset=True)

async def registerUser(
        username: str = Form(...),
        userpwd: str = Form(...),
        avatar: str | None = Form(None)):

        '''
        待补充email/手机号等
        '''
        usr_name,usr_pwd,usr_avatar = username, userpwd, avatar

        pwd_decrypt = decrypt_aes(usr_pwd,settings.KEY,settings.IV)
        ac_token = await register_user_handler(usr_name,pwd_decrypt,usr_avatar)

        return UserAuthRes(
            code = 200,
            msg = 'success',
            token = ac_token
        )

# 用户登陆
@user_rt.post(
        '/userLogin',
        response_model=UserAuthRes,
        response_model_exclude_unset=True)

async def loginUser(
        username: str = Form(...),
        userpwd: str = Form(...)):

        '''
        待补充email/手机号等
        '''
        usr_name, usr_pwd = username, userpwd
        pwd_decrypt = decrypt_aes(usr_pwd,settings.KEY,settings.IV)

        usr_login = await login_user_handler(usr_name,pwd_decrypt)
        token_data = create_actoken({'username':usr_login.usr_name})
        
        return UserAuthRes(code=200, msg='login success',token=token_data)
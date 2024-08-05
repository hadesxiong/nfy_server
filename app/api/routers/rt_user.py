# coding=utf8
from fastapi import APIRouter,Depends, Form
from fastapi.encoders import jsonable_encoder

from typing import Dict,Any

from app.api.schema.sch_user import UserInfoRes,UserInfoQuery
from app.api.controller.ctrl_user import get_userinfo_handler
from app.api.controller.ctrl_user import register_user_handler

from app.service.srv_security import decrypt_aes,get_pwd_hash,verify_pwd,get_current_user
from app.core.config import settings

# 定义查询路由
user_rt = APIRouter(
    prefix='/user',
    tags=['User','Basic Service'],
)

# 获取用户信息
@user_rt.get(
        '/getUserInfo',
        response_model=UserInfoRes,
        response_model_exclude_unset=True)

async def getUser(params: UserInfoQuery = Depends()):
        
    # 清理查询参数
        fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
        
        rst = await get_userinfo_handler(fltr_pars)

        print(rst)

        return UserInfoRes(
            data = rst.items,
            has_next = rst.page < rst.pages
        )

# 用户注册
@user_rt.post(
        '/userRegister',)

async def registerUser(
        username: str = Form(...),
        userpwd: str = Form(...),
        avatar: str | None = Form(None)):
        
        usr_name = username
        usr_pwd = userpwd
        usr_avatar = avatar

        pwd_decrypt = decrypt_aes(usr_pwd,settings.KEY,settings.IV)

        rst = await register_user_handler(usr_name,pwd_decrypt,usr_avatar)

        rst_2 = await get_current_user(rst)

        print(rst_2)

        return (rst)
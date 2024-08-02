# coding=utf8
from fastapi import APIRouter,Depends

from app.api.schema.sch_user import UserInfoRes,UserInfoQuery
from app.api.controller.ctrl_user import get_userinfo_handler

# 定义查询路由
user_rt = APIRouter(
    prefix='/User',
    tags=['User','Basic Service'],
)

@user_rt.get(
        '/getUserInfo',
        response_model=UserInfoRes,
        response_model_exclude_unset=True)

async def getUser(params:UserInfoQuery=Depends()):
        
    # 清理查询参数
        fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
        
        rst = await get_userinfo_handler(fltr_pars)

        print(rst)

        return UserInfoRes(
            data = rst.items,
            has_next = rst.page < rst.pages
        )
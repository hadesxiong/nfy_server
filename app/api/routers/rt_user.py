# coding=utf8
from fastapi import APIRouter,Depends,Body,Request

from app.api.schema.sch_user import UserInfoRes,UserInfoQuery
from app.api.controller.ctrl_user import get_userinfo_handler
from app.models import UserMain

# 定义查询路由
user_rt = APIRouter(
    prefix='/User',
    tags=['User','Basic Service'],
)

@user_rt.get(
        '/getUserInfo',
        response_model=UserInfoRes)

async def getUser(params:UserInfoQuery=Depends()):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
    
    rst = await get_userinfo_handler(fltr_pars)
    print(rst)

    return UserInfoRes(data = rst)
# coding=utf8
from fastapi import APIRouter,Depends,Body

from ..schema.basic import ResBasic

# 定义查询路由
common_rt = APIRouter(
    prefix='/common',
    tags=['common'],
)

@common_rt.get('/')

async def getUser():

    return ResBasic(code=200,msg='111',error='empty')
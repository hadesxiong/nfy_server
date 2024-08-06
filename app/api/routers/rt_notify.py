# coding=utf8
from fastapi import APIRouter,Depends,Request

from app.api.schema.sch_notfiy import ChannelUpdateQuery
from app.api.controller.ctrl_notfiy import *
from app.service.srv_security import get_current_user

# 定义路由
notify_rt = APIRouter(
    prefix='/notify',
    tags=['Notify','Config']
)

# 更新频道信息
@notify_rt.post(
    '/channelUpdate')

async def updateChannelInfo(
    form_data: ChannelUpdateQuery,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data = {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}

    rst = await update_channel_handler(
        channel_id=form_data.model_dump().get('chnl_id',None),
        channel_data=fltr_data,
        user=current_user)
    
    print(rst)

    return {'a':1}
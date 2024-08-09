# coding=utf8
from fastapi import APIRouter,Depends,Request
from typing import Dict,Any

from app.api.schema.sch_msg import MsgQueue
from app.api.controller.ctrl_msg import *
from app.service.srv_security import get_current_user

# 定义路由
msg_rt = APIRouter(
    prefix='/message',
    tags=['Notify','Push']
)

# 推送消息到rabbit服务
@msg_rt.post(
    '/sendMessage')

async def pushMsgQueue(
    form_data:MsgQueue,
    current_user: str = Depends(get_current_user)):

    rst = await push_msg_queue(
        chnl_id = form_data.chnl_id,
        tmpl_id = form_data.tmpl_id,
        msg_list = form_data.msg_list
    )

    
    return {'rst':1}

    # msg_list = [{'count': i} for i in range(1, 11)]

    # rst = await push_msg_queue(chnl_name='test',queue_name='test_queue',msg_list=msg_list)

    # return {'rst':rst}




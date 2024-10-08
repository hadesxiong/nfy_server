# coding=utf8
from fastapi import APIRouter,Depends,Request
from typing import Dict,Any

from app.api.schema.sch_msg import *
from app.api.controller.ctrl_msg import *
from app.service.srv_security import get_current_user

# 定义路由
msg_rt = APIRouter(prefix='/message',tags=['Notify','Push'])

# 推送消息到rabbit服务
@msg_rt.post('/sendMessage',
            response_model=MsgRes,
            response_model_exclude_unset=True)

async def pushMsgQueue(
    form_data:MsgQueue,
    current_user: str = Depends(get_current_user)):

    rst = await push_msg_queue(
        chnl_id = form_data.chnl_id,
        tmpl_id = form_data.tmpl_id,
        msg_dict = form_data.msg_dict,
        call_from = form_data.call_from
    )
    
    return MsgRes(code=200,msg='success',
                  receive_total_count=rst['rcv_length'],
                  template_title=rst['tmpl_title'],
                  channel_type=rst['chnl_type'])

# 查询消息记录
@msg_rt.get('/recordQuery',
            response_model=MsgRecRes,
            response_model_exclude_unset=True)

async def getMsgRecord(
    params: MsgRecQuery = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}

    rslt = await get_rec_handler(fltr_pars)

    return MsgRecRes(code=200,msg='success',
                     data=rslt.items,has_next=rslt.page<rslt.pages)
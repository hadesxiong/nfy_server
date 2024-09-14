# coding=utf8
from fastapi import APIRouter,Depends,Request

from app.api.schema.sch_config import ChannelUpdateQuery, TemplateUpdateQuery, UpdateRst
from app.api.controller.ctrl_config import *
from app.service.srv_security import get_current_user

# 定义路由
config_rt = APIRouter(prefix='/config', tags=['Notify','Config'])

# 更新频道信息
@config_rt.post(
        '/channelUpdate',
        response_model=UpdateRst,
        response_model_exclude_unset=True)

async def updateChannelInfo(
    form_data: ChannelUpdateQuery,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data = {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}
    
    rslt = await update_channel_handler(
        channel_id=form_data.model_dump().get('chnl_id',None),
        channel_data=fltr_data,
        user=current_user)
    
    return UpdateRst(code = 200, msg = 'success',
        target = rslt['id'],dt = rslt['dt'])

# 更新模板信息
@config_rt.post('/templateUpdate',
                response_model=UpdateRst,
                response_model_exclude_unset=True)

async def updateTemplateInfo(
    form_data: TemplateUpdateQuery,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data =  {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}

    rslt = await update_template_handler(
        template_id=form_data.model_dump().get('tmpl_id',None),
        template_data=fltr_data,
        user=current_user
    )

    return UpdateRst(code = 200, msg = 'success',
        target = rslt['id'],dt = rslt['dt'])


# 更新接收人信息
@config_rt.post('/receiverUpdate')

async def updateReceiverInfo(
    form_data:dict,
    current_user: str=Depends(get_current_user)):

    print(form_data)
    return form_data
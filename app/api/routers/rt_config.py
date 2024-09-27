# coding=utf8
from fastapi import APIRouter,Depends,Request

# from app.api.schema.sch_config import ChannelUpdateQuery, TemplateUpdateQuery, UpdateRst
# from app.api.schema.sch_config import ChannelQueryForm, ChannelInfoRes
# from app.api.schema.sch_config import TemplateQueryForm, TemplateInfoRes
from app.api.controller.ctrl_config import *
from app.api.schema.sch_config import *

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

# 查询频道信息
@config_rt.get('/channelQuery',
               response_model=ChannelInfoRes,
               response_model_exclude_unset=True)

async def getChannelInfo(
    params: ChannelQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}

    fltr_pars['chnl_update_dt'] = (
        fltr_pars.get('start_dt','1970-01-01'),
        fltr_pars.get('end_dt','2999-12-31')
    )
    
    fltr_pars.pop('start_dt',None)
    fltr_pars.pop('end_dt',None)

    if fltr_pars.get('chnl_id'):
        fltr_pars.pop('page_no',None)
        fltr_pars.pop('page_size',None)

    rslt = await get_channel_handler(fltr_pars)

    if fltr_pars.get('chnl_id'):
        return ChannelInfoRes(code=200,msg='success',data=rslt[0] if len(rslt)>=1 else None)
    else:
        return ChannelInfoRes(code=200,msg='success',data=rslt.items,has_next=rslt.page<rslt.pages)
    
# 查询模版信息
@config_rt.get('/templateQuery',
               response_model=TemplateInfoRes,
               response_model_exclude_unset=True)

async def getTemplateInfo(
    params: TemplateQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}

    fltr_pars['tmpl_update_dt'] = (
        fltr_pars.get('start_dt','1970-01-01'),
        fltr_pars.get('end_dt','2999-12-31')
    )
    
    fltr_pars.pop('start_dt',None)
    fltr_pars.pop('end_dt',None)

    if fltr_pars.get('tmpl_id'):
        fltr_pars.pop('page_no',None)
        fltr_pars.pop('page_size',None)

    rslt = await get_template_handler(fltr_pars)

    if fltr_pars.get('tmpl_id'):
        return TemplateInfoRes(code=200,msg='success',data=rslt[0] if len(rslt)>=1 else None)
    else:
        return TemplateInfoRes(code=200,msg='success',data=rslt.items,has_next=rslt.page<rslt.pages)
    
# 查询用户信息
@config_rt.get('/receiverQuery')

async def getReceiverInfo(
    params: ReceiverQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
    
    if fltr_pars.get('target_id'):
        fltr_pars.pop('page_no',None)
        fltr_pars.pop('page_size',None)

    if int(fltr_pars['target_class']) == 1:
        fltr_pars['rcv_id'] = fltr_pars.get('target_id',None)
        if not fltr_pars.get('rcv_id'):
            fltr_pars.pop('rcv_id',None)
        fltr_pars.pop('target_id',None)
        fltr_pars.pop('group_name',None)
        fltr_pars.pop('target_class',None)

        rslt = await get_receiver_handler(fltr_pars)
    
    elif int(fltr_pars['target_class']) == 2:
        fltr_pars['group_id'] = fltr_pars.get('target_id',None)
        if not fltr_pars.get('group_id'):
            fltr_pars.pop('group_id',None)
        fltr_pars.pop('target_id',None)
        fltr_pars.pop('rcv_chnl',None)
        fltr_pars.pop('rcv_type',None)
        fltr_pars.pop('target_class',None)

        rslt = await get_rcvgroup_handler(fltr_pars)

    print(rslt)


    return {'1':1}


# coding=utf8
from fastapi import APIRouter,Depends,Request
from typing import Union
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
@config_rt.post('/receiverUpdate',
                response_model=UpdateRst,
                response_model_exclude_unset=True)

async def updateReceiverInfo(
    form_data:ReceiverUpdateForm,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data =  {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}
    rslt = await update_receiver_handler(
        receiver_id=form_data.model_dump().get('rcv_id',None),
        receiver_type=form_data.model_dump().get('rcv_type',None),
        receiver_channel=form_data.model_dump().get('rcv_chnl',None),
        receiver_data=fltr_data,
        user=current_user
    )

    return UpdateRst(code = 200, msg = 'success',
        target = rslt['id'], dt = rslt['dt'])

# 更新接受群组
@config_rt.post('/rcvGroupUpdate',
                response_model=UpdateRst,
                response_model_exclude_unset=True)

async def updateRcvGroupInfo(
    form_data:RcvGroupUpdate,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data = {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}
    rslt = await update_rcvgroup_handler(
        group_id=form_data.model_dump().get('group_id',None),
        group_data=fltr_data,
        user=current_user)

    return UpdateRst(code=200,msg='success',
                     target=rslt['id'],dt=rslt['dt'])

# 更新接受群组人员明细
@config_rt.post('/rcvGroupDetailUpdate',
                response_model=UpdateRst,
                response_model_exclude_unset=True)

async def updateRcvGroupDetail(
    form_data: GroupDetailUpdate,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data = {k:v for k,v in form_data.model_dump()['group_data'].items() if v is not None}

    rslt = await update_grouplist_handler(
        group_id= form_data.model_dump().get('group_id',None),
        rcv_dict = fltr_data,
        user=current_user,
    )

    return UpdateRst(code=200,msg='success',dt=rslt['dt'],
            target={'delete':rslt['remove'],'add':rslt['insert']})

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
@config_rt.get('/receiverQuery',
               response_model=ReceiverListRes,
               response_model_exclude_unset=True)

async def getReceiverInfo(
    params: ReceiverQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}
    
    rslt = await get_receiver_handler(fltr_pars)
    
    if not fltr_pars.get('rcv_id'):
        return ReceiverListRes(
            code=200,msg='success',data=rslt.items,
            has_next=rslt.page<rslt.pages
        )

    else:
        return ReceiverListRes(
            code=200,msg='success',
            data=rslt[0] if len(rslt) >=1 else None
        )

# 查询分组基本信息
@config_rt.get('/rcvGroupQuery',
               response_model=ReceiverListRes,
               response_model_exclude_unset=True)

async def getRcvGroupInfo(
    params: RcvGroupQueryForm = Depends(),
    current_use: str = Depends(get_current_user)):

    # 清理查询参数
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}

    rslt = await get_rcvgroup_handler(fltr_pars)
    print(rslt)
    if not fltr_pars.get('group_id'):
        return ReceiverListRes(
            code=200,msg='success',data=rslt.items,
            has_next=rslt.page<rslt.pages
        )
    else:
        return ReceiverListRes(
            code=200,msg='success',
            data=rslt[0] if len(rslt) >=1 else None
        )

# 查询分组明细
@config_rt.get('/rcvGroupDetailQuery',
               response_model=ReceiverListRes,
               response_model_exclude_unset=True)

async def getRcvGroupDetail(
    params: RcvGroupDetailQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    # 清理查询参数,
    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None and k == 'target_id'}

    if fltr_pars.get('target_id',None):

        result = await get_rcvgourp_detail_handler(fltr_pars)
        return ReceiverListRes(code=200,msg='success',data=result)
    else:
        return ReceiverListRes(code=300,msg='failed')
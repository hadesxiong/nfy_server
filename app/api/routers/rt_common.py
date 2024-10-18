# coding=utf8

from fastapi import APIRouter,Depends

from app.api.controller.ctrl_common import *
from app.api.schema.sch_common import *
from app.service.srv_security import get_current_user

# 定义路由
common_rt = APIRouter(prefix='/common', tags=['Common'])

# 查询字典信息
@common_rt.get(
    '/dictQuery',
    response_model=DictListRes,
    response_model_exclude_unset=True)

async def getDictInfo(
    params: DictQueryForm = Depends(),
    current_user: str = Depends(get_current_user)):

    fltr_pars = {k:v for k,v in params.model_dump().items() if v is not None}

    if fltr_pars.get('mark_id'):
        fltr_pars.pop('page_no',None)
        fltr_pars.pop('page_size',None)

    rslt = await get_dict_handler(fltr_pars)

    if fltr_pars.get('mark_id'):
        return DictListRes(code=200, msg='success', data = rslt[0] if len(rslt)>=1 else None)
    else:
        return DictInfoRes(code=200, msg='success', data = rslt.items, has_next=rslt.page<rslt.pages)


# 更新字典信息
@common_rt.post(
    '/dictUpdate',
    response_model=UpdateRst,
    response_model_exclude_unset=True)

async def updateDictInfo(
    form_data: DictUpdate,
    current_user: str = Depends(get_current_user)):

    # 清理参数
    fltr_data = {k:v for k,v in form_data.model_dump()['form'].items() if v is not None}
    rslt = await update_dict_handler(
        mark_id=form_data.model_dump().get('mark_id',None),
        mark_data=fltr_data,
        user=current_user
    )

    return UpdateRst(code=200,msg='success',
                     target=rslt['id'],dt=rslt['dt'])
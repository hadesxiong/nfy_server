# coding=utf8
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from typing import Dict,Any
from tortoise.expressions import Q
from datetime import datetime,timezone,timedelta
from bson.objectid import ObjectId

from app.models.notify import NfyChnl
from app.utils.query import build_query_exp
from app.api.controller.ctrl_error import CustomHTTPException

# 创建/更新频道
async def update_channel_handler(
        channel_id: str | None = None, 
        channel_data: Dict[str,Any] | None = None, 
        user: str | None = None,):
    
    # 如果传入channel_id则为更新,反之则为创建
    if channel_id:
        
        try:
            chnl_ins = await NfyChnl.get(Q(chnl_id=channel_id))
            update_fields = {}
            
            for k,v in channel_data.items():
                if v is not None and v != getattr(chnl_ins,k):
                    update_fields[k] = v

            if len(update_fields) > 0:   
                update_fields['chnl_update_usr'] = user
                update_fields['chnl_update_dt'] = datetime.now(timezone(timedelta(hours=8)))
                # chnl_rst = await NfyChnl.filter(Q(chnl_id=channel_id)).update(**update_fields)
                chnl_rst = await chnl_ins.save(update_fields=update_fields)
                return chnl_rst

            else:
                raise CustomHTTPException(
                    status_code = 400,
                    detail = '无更新数据',
                    err_code = 12001
                )
        
        except:
            raise CustomHTTPException(
                status_code = 400,
                detail = '数据不合法',
                err_code = 12002
            )


    elif channel_id is None and len(channel_data) != 0:

        try:
            chnl_dt = datetime.now(timezone(timedelta(hours=8)))
            channel_data.update({
                'chnl_id': f'chnl_{ObjectId()}',
                'chnl_create_usr': user,
                'chnl_creaet_dt': chnl_dt,
                'chnl_update_usr': user,
                'chnl_update_dt': chnl_dt
            })

            chnl_rst = await NfyChnl.create(**channel_data)
            return chnl_rst
        
        except:
            raise CustomHTTPException(
                status_code = 400,
                detail = '数据不合法',
                err_code =12003
            )
        
    else:
        raise CustomHTTPException(
            status_code = 400,
            detail = '数据异常',
            err_code = 12004
        )
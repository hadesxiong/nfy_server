# coding=utf8
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from typing import Dict,Any
from tortoise.expressions import Q
from datetime import datetime,timezone,timedelta
from bson.objectid import ObjectId

from app.models.notify import NfyChnl,NfyTmpl
from app.models.receiver import RcvMain,RcvBark, RcvNtfy, RcvGroup
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
                
                for field,value in update_fields.items():
                    setattr(chnl_ins,field,value)
                
                await chnl_ins.save()
                return {
                    'id':chnl_ins.chnl_id[5:],
                    'dt':update_fields['chnl_update_dt'].strftime('%Y-%m-%d %H:%M:%S')
                }

            else:
                raise CustomHTTPException(status_code = 400, detail = '无更新数据', err_code = 12001)
        
        except:
            raise CustomHTTPException(status_code = 400, detail = '数据不合法', err_code = 12002)

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

            chnl_rslt = await NfyChnl.create(**channel_data)
            return {
                'id': chnl_rslt.chnl_id[5:],
                'dt': chnl_dt.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except:
            raise CustomHTTPException(status_code = 400, detail = '数据不合法', err_code =12003)
        
    else:
        raise CustomHTTPException(status_code = 400, detail = '数据异常', err_code = 12004)
    
# 创建/更新模板
async def update_template_handler(
        template_id: str | None = None,
        template_data: Dict[str,Any] | None = None,
        user: str | None = None):
    
    # 如果传入tmpl_id为更新, 反之则为创建
    if template_id:

        try:
            tmpl_ins = await NfyTmpl.get(Q(tmpl_id=template_id))
            update_fields = {}

            for k,v in template_data.items():
                print(k,v)
                if v is not None and v != getattr(tmpl_ins,k):
                    update_fields[k] = v

            if len(update_fields) > 0:
                update_fields['tmpl_update_usr'] = user
                update_fields['tmpl_update_dt'] = datetime.now(timezone(timedelta(hours=8)))
                
                for field,value in update_fields.items():
                    setattr(tmpl_ins,field,value)

                await tmpl_ins.save()
                return {
                    'id': tmpl_ins.tmpl_id[5:],
                    'dt': update_fields['tmpl_update_dt'].strftime('%Y-%m-%d %H:%M:%S')
                }
            
            else:
                raise CustomHTTPException(status_code = 400, detail = '无更新数据', err_code = 12001)
            
        except:
            raise CustomHTTPException(status_code = 400, detail = '数据不合法', err_code = 12002)

    elif template_id is None and len(template_data) != 0:

        try:
            tmpl_dt = datetime.now(timezone(timedelta(hours=8)))
            template_data.update({
                'tmpl_id': f'tmpl_{ObjectId()}',
                'tmpl_create_usr': user,
                'tmpl_create_dt': tmpl_dt,
                'tmpl_update_usr': user,
                'tmpl_update_dt': tmpl_dt
            })

            tmpl_rslt = await NfyTmpl.create(**template_data)
            return {
                'id': tmpl_rslt.tmpl_id[5:],
                'dt': tmpl_dt.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except:
            raise CustomHTTPException(status_code = 400, detail = '数据不合法', err_code =12003)
        
    else:
        raise CustomHTTPException(status_code = 400, detail = '数据异常', err_code = 12004)
    
# 创建/更新用户
async def update_receiver_handler(
        receiver_id: str | None = None,
        receiver_data: Dict[str,Any] | None = None,
        user: str | None = None):
    
    # 如果传入receiver_id为修改，反之则为创建
    if receiver_id:
        
        try:
            rcvMain_ins = RcvMain.get(Q(rcv_id=receiver_id))
            if rcvMain_ins.rcv_type == 1:
                rcv_ins = RcvBark.get(Q(rcv_id=receiver_id))
            elif rcvMain_ins.rcv_type == 2:
                rcv_ins = RcvNtfy.get(Q(rcv_id=receiver_id))

            update_fields = {}
            main_update_fields = {}
            for k,v in receiver_data.items():
                if v is not None and v != getattr(rcv_ins,k):
                    update_fields[k] = v          

            if len(update_fields) > 0:
                main_update_fields['rcv_update_usr'] = user
                main_update_fields['rcv_update_dt'] = datetime.now(timezone(timedelta(hours=8)))

                for field, value in update_fields.items():
                    setattr(rcv_ins,field,value)

                await rcv_ins.save()
                
                for field, value in main_update_fields.items():
                    setattr(rcvMain_ins,field,value)

                await rcvMain_ins.save()

                return {
                    'id': rcvMain_ins.rcv_id[4:],
                    'dt': main_update_fields['rcv_update_dt'].strftime('%Y-%m-%d %H:%M:%S')
                }
            
            else:
                raise CustomHTTPException(status_code = 400, detail = '无更新数据', err_code = 12001)
        
        except:
            raise CustomHTTPException(status_code = 400, detail = '数据不合法', err_code = 12002)
    
    elif receiver_id is None and len(receiver_data) != 0:
        print('chuangjian')

    else:
        raise CustomHTTPException(status_code = 400, detail = '数据异常', err_code = 12004)

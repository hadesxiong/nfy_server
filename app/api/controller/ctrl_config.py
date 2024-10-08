# coding=utf8
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from typing import List,Dict,Any
from tortoise.expressions import Q
from datetime import datetime,timezone,timedelta
from bson.objectid import ObjectId

from app.models.notify import NfyChnl,NfyTmpl
from app.models.receiver import RcvMain,RcvBark, RcvNtfy, RcvGroup
from app.utils.query import build_query_exp, build_or_exp, distinct_query,paginate_query
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
        receiver_type: int | None = None,
        receiver_channel: str | None = None,
        receiver_data: Dict[str,Any] | None = None,
        user: str | None = None):
    
    # 如果传入receiver_id为修改，反之则为创建
    if receiver_id:
        
        try:
            rcvMain_ins = await RcvMain.get(Q(rcv_id=receiver_id))
            if rcvMain_ins.rcv_type == 1:
                rcv_ins = await RcvBark.get(Q(rcv_id=receiver_id))
            elif rcvMain_ins.rcv_type == 2:
                rcv_ins = await RcvNtfy.get(Q(rcv_id=receiver_id))

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
        try:
            rcv_dt = datetime.now(timezone(timedelta(hours=8)))
            rcvMain_new = {
                'rcv_id': f'rcv_{ObjectId()}',
                'rcv_channel': receiver_channel,
                'rcv_type': receiver_type,
                'rcv_create_dt': rcv_dt,
                'rcv_update_dt': rcv_dt,
                'rcv_create_usr': user,
                'rcv_update_usr': user
            }

            receiver_data.update({
                'rcv_id': rcvMain_new['rcv_id']
            })

            try:
                if receiver_type == 1:
                    rcv_rslt = await RcvBark.create(**receiver_data)
                elif receiver_type == 2:
                    rcv_rslt = await RcvNtfy.create(**receiver_data)
                else:
                    raise CustomHTTPException(status_code = 400, detail='数据不合法', err_code=12006)

                rcvMain_rslt = await RcvMain.create(**rcvMain_new)

                return {
                    'id': rcvMain_rslt.rcv_id[4:],
                    'dt': rcv_dt.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            except:
                raise CustomHTTPException(status_code = 400, detail='数据不合法', err_code=12007)

        except:
            raise CustomHTTPException(status_code = 400, detail='数据不合法',err_code = 12005)

    else:
        raise CustomHTTPException(status_code = 400, detail = '数据异常', err_code = 12004)

# 创建/更新群组 - 基本信息
async def update_rcvgroup_handler(
        group_id: str | None = None,
        group_data: Dict[str,Any] | None = None,
        user: str | None = None):
    
    # 如果传入receiver_id那么就是新增, 反之则为创建
    if group_id:

        try:
            group_ins = await RcvGroup.filter(group_id=group_id).first()
            
            update_fields = {}
            for k,v in group_data.items():
                if v is not None and v != getattr(group_ins,k):
                    update_fields[k] = v

            if len(update_fields) > 0:
                
                update_fields['group_update_usr'] = user
                update_fields['group_update_dt'] = datetime.now(timezone(timedelta(hours=8)))

                for field, value in update_fields.items():
                    setattr(group_ins,field,value)

                await group_ins.save()
                return {
                    'id': group_ins.group_id[6:],
                    'dt': update_fields['group_update_dt']
                }

            else:
                raise CustomHTTPException(status_code = 400, detail='无更新数据',err_code=12001)

        except:
            raise CustomHTTPException(status_code = 400, detail='数据不合法', err_code=12002)

    elif group_id is None and len(group_data) != 0:

        try:

            group_dt = datetime.now(timezone(timedelta(hours=8)))
            group_data.update({
                'group_id': f'group_{ObjectId()}',
                'group_create_usr': user,
                'group_create_dt': group_dt,
                'group_update_usr': user,
                'group_update_dt': group_dt
            })

            group_rslt = await RcvGroup.create(**group_data)
            return {
                'id': group_rslt.group_id[6:],
                'dt': group_dt.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except:
            raise CustomHTTPException(status_code=400, detail='数据不合法', err_code=12004)

    else:
        raise CustomHTTPException(status_code=400,detail='数据异常',err_code=12005)

# 创建/更新群组 - 成员
# async def update_grouplist_handler(
#         group_id:str,rcv_dict:Dict[str,Any],user:str | None = None):
    


# 查询频道
async def get_channel_handler(filters):

    '''
    调整filters
    1. start_dt ,end_dt 调整为(start_dt,end_dt)
    2. key_word 剥离另外查询
    '''

    channel_logic = {'chnl_update_dt':'range'}
    or_query = Q()

    if filters.get('key_word'):
        or_query |= build_or_exp(
            ['chnl_id','chnl_name','chnl_host','chnl_update_usr'],
            filters.get('key_word'))
        
        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    and_query = build_query_exp(filter_dict,channel_logic)

    order_dict = {
        'id':'chnl_id','-id':'-chnl_id','name':'chnl_name','-name':'-chnl_name',
        'stu':'chnl_stu','-stu':'-chnl_stu','type':'chnl_type','-type':'-chnl_type',
        'dt':'chnl_update_dt','-dt':'-chnl_update_dt'
    }
    order_index = order_dict.get(filters.get('order_by'),'-chnl_update_dt')

    try:
        if filters.get('page_no'):
            chnl_rslt = await paginate(
                NfyChnl.filter(and_query).filter(or_query).order_by(order_index),
                Params(page=filters['page_no'],size=filters['page_size'])
            )
        else:
            chnl_rslt = await NfyChnl.filter(and_query).filter(or_query)

        return chnl_rslt
    
    except:
        raise CustomHTTPException(status_code=400,detail='查询参数错误',err_code=12003)
    
# 查询模版
async def get_template_handler(filters):

    # 逻辑相似，轻易get_channel_handler为准
    template_logic = {'tmpl_update_dt':'range'}
    or_query = Q()

    if filters.get('key_word'):
        or_query |= build_or_exp(
            ['tmpl_id','tmpl_chnl','tmpl_title','tmpl_update_usr'],
            filters.get('key_word')
        )

        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    and_query = build_query_exp(filter_dict,template_logic)

    order_dict = {
        'id':'tmpl_id','-id':'-tmpl_id','title':'tmpl_title','-title':'-tmpl_title',
        'dt':'tmpl_update_dt','-dt':'-tmpl_update_dt'
    }

    order_index = order_dict.get(filters.get('order_by'),'-tmpl_update_dt')

    try:
        if filters.get('page_no'):
            tmpl_rslt = await paginate(
                NfyTmpl.filter(and_query).filter(or_query).order_by(order_index),
                Params(page=filters['page_no'],size=filters['page_size'])
            )
        else:
            tmpl_rslt = await NfyTmpl.filter(and_query).filter(or_query)

        return tmpl_rslt
    
    except:
        raise CustomHTTPException(status_code=400,detail='查询参数错误',err_code=12004)
    
# 查询用户
async def get_receiver_handler(filters):

    receiver_logic = {'rcv_update_dt':'range'}
    or_query = Q()

    if filters.get('key_word'):
        or_query |= build_or_exp(
            ['rcv_id','rcv_chnl','rcv_update_usr'],
            filters.get('key_word')
        )

        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    and_query = build_query_exp(filter_dict,receiver_logic)

    order_dict = {
        'id':'rcv_id','-id':'-rcv_id','channel':'rcv_chnl','-channel':'-rcv_channel',
        'dt':'rcv_update_dt','-dt':'-rcv_update_dt'
    }

    order_index = order_dict.get(filters.get('order_by'),'-rcv_update_dt')

    try:
        if filters.get('page_no'):
            rcv_rslt = await paginate(
                RcvMain.filter(and_query).filter(or_query).order_by(order_index),
                Params(page=filters['page_no'],size=filters['page_size'])
            )
        else:
            rcv_rslt = await RcvMain.filter(and_query).filter(or_query)

        return rcv_rslt

    except:
        raise CustomHTTPException(status_code=400,detail='查询参数错误',err_code='12005')
    
# 查询分组
async def get_rcvgroup_handler(filters):

    rcvgroup_logic = {'group_update_dt':'range'}
    or_query = Q()

    if filters.get('key_word'):
        or_query |= build_or_exp(
            ['group_id','group_name','group_update_usr'],
            filters.get('key_word')
        )
        
        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    and_query = build_query_exp(filter_dict,rcvgroup_logic)

    order_dict = {
        'id':'group_id','-id':'-group_id','name':'group_name','-name':'-group_name',
        'dt':'group_update_dt','-dt':'-group_update_dt'
    }
    
    order_index = order_dict.get(filters.get('order_by'),'group_update_dt')

    group_query = RcvGroup.filter(and_query).filter(or_query).order_by(order_index)
    group_distinct = await distinct_query(group_query,'group_id','group_name')

    try:
        if filters.get('page_no'):
            group_rslt = await paginate_query(group_distinct,filters['page_no'],filters['page_size'])

        else:
            group_rslt = group_distinct[0] if len(group_distinct) > 0 else []

        return group_rslt
    
    except:
        raise CustomHTTPException(status_code=400,detail='查询参数错误',err_code=12006)
    
# 查询分组明细
async def get_rcvgourp_detail_handler(filters):

    try:
        group_id = filters.get('target_id',None)
        group_ins = await RcvGroup.filter(group_id=group_id).first()
        group_rcv = await RcvGroup.filter(group_id=group_id).values_list('group_rcv',flat=True)
        group_ins.group_rcv = group_rcv
        
        return group_ins

    except:
        raise CustomHTTPException(status_code=400,detail='查询参数错误',err_code=12007)
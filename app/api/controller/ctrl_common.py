# coding=utf8

from bson.objectid import ObjectId
from datetime import datetime,timezone,timedelta
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from typing import Dict,Any
from tortoise.expressions import Q

from app.models.common import DictMark
from app.utils.query import build_query_exp, build_or_exp
from app.api.controller.ctrl_error import CustomHTTPException

# 查询字典
async def get_dict_handler(filters):

    or_query = Q()

    if filters.get('key_word'):

        or_query |= build_or_exp(
            ['mark_index','mark_value','mark_abbr'],
            filters.get('key_word'))
        
        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    print(filter_dict)

    and_query = build_query_exp(filter_dict)

    order_dict = {
        'id':'mark_id','-id':'-mark_id','code':'marK_code','-code':'-mark_code',
        'value':'mark_value','-value':'-mark_value','name':'mark_abbr','-name':'-mark_abbr'
    }

    order_index = order_dict.get(filters.get('order_by'),'-id')

    try:
        if filters.get('page_no'):
            dict_rslt = await paginate(
                DictMark.filter(and_query).filter(or_query).order_by(order_index),
                Params(page=filters['page_no'],size=filters['page_size'])
            )
        else:
            dict_rslt = await DictMark.filter(and_query).filter(or_query)

        return dict_rslt
    
    except:
        raise CustomHTTPException(status_code=400, detail='查询参数错误', err_code=12003)
    
# 更新字典
async def update_dict_handler(
        mark_id: str | None = None,
        mark_data: Dict[str,Any] | None = None,
        user: str | None = None):
    
    # 如果传入mark_id则为更新，反之则为创建
    if mark_id:

        try:
            mark_ins = await DictMark.get(Q(mark_id=mark_id))
            update_fields = {}

            for k,v in mark_data.items():
                if v is not None and v != getattr(mark_ins,k):
                    update_fields[k] = v

            if len(update_fields) > 0:
                
                for field,value in update_fields.items():
                    setattr(mark_ins,field,value)

                await mark_ins.save()
                return {
                    'id': mark_ins.mark_id,
                    'dt': datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
                }
            
            else:
                raise CustomHTTPException(status_code=400,detail='无更新数据',err_code=12004)
        
        except:
            raise CustomHTTPException(status_code=400, detail='数据不合法', err_code=12005)
        
    elif mark_id is None and len(mark_data) != 0:

        try:
            mark_data.update({'mark_id':f'dict_{ObjectId()}'})
            mark_rslt = await DictMark.create(**mark_data)

            return {
                'id': mark_rslt.mark_id,
                'dt': datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except:
            raise CustomHTTPException(status_code=400, detail='数据不合法', err_code=12006)
        
    else:
        raise CustomHTTPException(status_code=400, detail='数据异常', err_code=12007)

# coding=utf8
from app.models.common import UserMain

from app.utils.query import build_query_exp

from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
# from fastapi_pagination import paginate

async def get_userinfo_handler(filters):

    '''
    查询方法:
    1. filters由外部做初步过滤后传入
    2. logics为每个handler自定义
    3. 传入的filters包含page_no,page_size,需要过滤
    '''
    '''
    userInfo的运算逻辑:(默认为equal)
    1. contains: usr_name
    '''

    user_logics = {'usr_name':'contains'}
    fltr_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    filter_query = build_query_exp(fltr_dict,user_logics)

    order_dict = {
        'id':'usr_id','-id':'-usr_id',
        'name': 'usr_name','-name':'-usr_name',
        'stu':'usr_stu','-stu':'-usr_stu',
        'role':'usr_role','-role':'-usr_role',
        'dt':'usr_create_dt','-dt':'-usr_create_dt'
    }

    order_index = order_dict.get(filters.get('order_by'),'-usr_create_dt')

    user_rslt = await paginate(
        UserMain.filter(filter_query).order_by(order_index),
        Params(page=filters['page_no'],size=filters['page_size'])
    )

    return user_rslt
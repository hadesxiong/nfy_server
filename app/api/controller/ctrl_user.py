# coding=utf8
from app.models.common import UserMain, UserAuth

from app.utils.query import build_query_exp
from app.service.srv_security import get_user,get_pwd_hash, create_actoken, get_current_user
from app.api.controller.ctrl_error import CustomHTTPException

from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate

from datetime import datetime,timezone,timedelta

from bson.objectid import ObjectId

# 查询用户信息
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

# 用户注册
async def register_user_handler(
        usr_name:str, usr_pwd: str, usr_avatar: str):
    
    '''
    业务逻辑
    1. 查询用户名是否重复, 如果重复直接抛出错误, 如果不重复继续
    2. 用户id通过bson.objects.ObjectId()方法生成, 前缀为usr_
    3. 默认的用户role始终为1 - 普通用户；
    4. 默认的用户stu始终为1 - 正常；
    5. 默认的用户auth_type为1 - 密码登陆;
    6. usr_pwd被定义在UserAuth中进行存储
    '''

    if not get_user(UserMain, usr_name):

        user_id = f'usr_{str(ObjectId())}'
        user_update_dt = datetime.now(timezone(timedelta(hours=8)))

        userMain_data = {
            'usr_id': user_id,'usr_name':usr_name,
            'usr_role':1, 'usr_stu':1, 'usr_auth_type':1,
            'usr_avatar': usr_avatar if usr_avatar is not None else 'blank',
            'usr_create_dt': user_update_dt
        }

        userAuth_data = {
            'usr_id': user_id, 'usr_name': usr_name,
            'usr_pwd': get_pwd_hash(usr_pwd),
            'auth_update_dt': user_update_dt
        }

        try:

            # userMain_ins = await UserMain.create(**userMain_data)
            # userAuth_ins = await UserAuth.create(**userAuth_data)

            token_data = create_actoken({'username':usr_name})

            print(token_data)

            # result_token = await get_current_user(token_data)
            # print(get_current_user(token_data))
            # print(result_token)

            # return {'user_id': user_id}
            return token_data
        
        except Exception as e:

            raise CustomHTTPException(
                status_code=400, 
                detail='用户已存在', 
                err_code= 11002)

    else:

        return {'1':1}
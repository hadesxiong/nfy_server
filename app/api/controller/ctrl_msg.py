# coding=utf8
import json
from fastapi import status
from fastapi_pagination import Params
from fastapi_pagination.ext.tortoise import paginate
from aio_pika import Message
from bson import ObjectId
from app.core.rabbit import create_rb_channel

from tortoise.expressions import Q

# 引入模型
from app.models.notify import NfyChnl,NfyTmpl,NfyRec
from app.models.receiver import RcvBark,RcvNtfy,RcvGroup
from app.api.schema.sch_msg import MsgData

# 引入错误内容
from app.api.controller.ctrl_error import CustomHTTPException

from app.utils.query import build_query_exp,build_or_exp,paginate_query

# 推送消息到rabbit
async def push_msg_queue(chnl_id:str, tmpl_id: str, msg_dict: MsgData, call_from: str) -> str:

    try:
        chnl_ins = await NfyChnl.get(chnl_id=chnl_id)
        tmpl_ins = await NfyTmpl.get(tmpl_id=tmpl_id)

        rb_chnl_ins = await create_rb_channel()
        
        await rb_chnl_ins.declare_queue(name = chnl_ins.chnl_id, durable = True)
        
        # 定义表头
        msg_headers = {
            'chnl_type': chnl_ins.chnl_type,
            'chnl_auth_data': chnl_ins.chnl_auth_data,
            'chnl_auth_method': chnl_ins.chnl_auth_method,
            'chnl_host': chnl_ins.chnl_host,
            'tmpl_id': tmpl_ins.tmpl_id,
            'tmpl_title': tmpl_ins.tmpl_title,
            'tmpl_args': tmpl_ins.tmpl_args,
            'call_from': call_from,
            'batch_id': f'batch_{ObjectId()}'
        }
        # 定义其他属性
        msg_properties = {
            'app_id': 'nfy_server',
            'content_type': 'application/json',
            'delivery_mode':2
        }

        # 判断推送模式
        # 推送模式1: 向全体接收者发送相同的信息
        # 推送模式2: 向每个接收者发送匹配数据的信息

        message_data = msg_dict.model_dump()
 
        if msg_headers['chnl_type'] == 1 and message_data['msg_rcv'] == 'all':
            rcv_list = await RcvBark.all()
        elif msg_headers['chnl_type'] == 1 and message_data['msg_rcv'] == 'single':
            rcv_list = await RcvBark.filter(rcv_id=f'rcv_{message_data["msg_target"]}')
        elif msg_headers['chnl_type'] == 1 and message_data['msg_rcv'] == 'group':
            rcv_group = await RcvGroup.filter(group_id=f'group_{message_data["msg_target"]}').values_list('group_rcv',flat=True)
            rcv_list = await RcvBark.filter(rcv_id__in=rcv_group).all()
        elif msg_headers['chnl_type'] == 2 and message_data['msg_rcv'] == 'all':
            rcv_list = await RcvNtfy.all()
        elif msg_headers['chnl_type'] == 2 and message_data['msg_rcv'] == 'single':
            rcv_list = await RcvNtfy.filter(rcv_id=f'rcv_{message_data["msg_target"]}')
        elif msg_headers['chnl_type'] == 2 and message_data['msg_rcv'] == 'group':
            rcv_group = await RcvGroup.filter(group_id=f'group_{message_data["msg_target"]}').values_list('group_rcv',flat=True)
            rcv_list = await RcvNtfy.filter(rcv_id__in=rcv_group).all()
        else:
            raise CustomHTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,detail='频道错误',err_code=13001)

        for each in rcv_list:

            if msg_headers['chnl_type'] == 1:
                msg_body = {
                    'receive': {
                        'id': each.rcv_id,
                        'device': each.device_key,
                        'key': each.rcv_key,
                        'iv': each.rcv_iv
                    },
                    'detail': message_data['msg_data'],
                    'url_args': message_data['msg_url_data']
                }

            elif msg_headers['chnl_type'] == 2:
                msg_body = {
                    'receive': {
                        'id': each.rcv_id,
                        'name': each.rcv_name,
                        'topic': each.rcv_topic,
                        'role': each.rcv_role
                    },
                    'detail': message_data['msg_data'],
                    'url_args': message_data['msg_url_data']
                }

            msg_body = json.dumps(msg_body).encode('utf-8')
            msg_ins = Message(headers= msg_headers, body=msg_body, **msg_properties)
            await rb_chnl_ins.default_exchange.publish(msg_ins,routing_key= chnl_ins.chnl_id)

    except Exception as e:

            raise CustomHTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,detail = '频道模板错误',err_code = 13002)

    finally:

        await rb_chnl_ins.close()

    return {
        'rcv_length': len(rcv_list),
        'chnl_type':msg_headers['chnl_type'],
        'tmpl_title':tmpl_ins.tmpl_title
    }
    # 使用 create_rb_channel 获取通道实例，并自动管理其生命周期
    # chnl_ins = await create_rb_channel()
    # try:
    #     await chnl_ins.declare_queue(name=queue_name, durable=True)
    #     for msg_data in msg_list:
    #         msg_body = json.dumps(msg_data).encode('utf-8')
    #         msg_ins = Message(body=msg_body)
    #         await chnl_ins.default_exchange.publish(
    #             msg_ins, routing_key=queue_name)
    # finally:
    #     # 确保通道被关闭
    #     await chnl_ins.close()
    # return 'success'

# 定义获取所有的chnl_id用于消费函数启动监听
async def get_chnl_list() -> list:

    # 使用annotate和values来获取所有chnl_id
    chnl_ids = await NfyChnl.all().values_list('chnl_id', flat=True)
    return chnl_ids

# 定义方法用来调用存储推送结果
async def set_rec_data(rec_dict:dict) -> str:

    # 存储rec_dict
    rec_ins = await NfyRec.create(**rec_dict)
    await rec_ins.save()

    return rec_ins.rec_id[4:]

# 定义方法用来获取发送记录
async def get_rec_handler(filters):

    record_logic = {}

    or_query = Q()
    if filters.get('key_word'):
        or_query |= build_or_exp(
            ['rec_id','tmpl_id','rec_use','rec_msg','rec_data','rec_rcv','rec_batch'],
            filters.get('key_word')
        )

        filters.pop('key_word',None)

    filter_dict = {
        k:v for k,v in filters.items() \
        if k not in ['page_no','page_size','order_by']
    }

    and_query = build_query_exp(filter_dict,record_logic)

    order_dict = {
        'id':'rec_id','-id':'-rec_id','template':'tmpl_id','-template':'-tmpl_id',
        'receiver':'rec_rcv','-receiver':'-rec_rcv',
        'batch':'rec_batch','-batch':'-rec_batch',
        'code':'rec_code','-code':'-rec_code'
    }

    order_index = order_dict.get(filters.get('order_by'),'-rec_id')

    rec_rlst= await paginate(
        NfyRec.filter(and_query).filter(or_query).order_by(order_index),
        Params(page=filters['page_no'],size=filters['page_size'])
    )

    return rec_rlst

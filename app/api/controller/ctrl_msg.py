# coding=utf8
import json
from fastapi import status
from typing import List
from aio_pika import RobustChannel, Message
from app.core.rabbit import create_rb_channel

# 引入模型
from app.models.notify import NfyChnl,NfyTmpl

# 引入推送逻辑
from app.service.srv_bark import send_bark_nfy
from app.service.srv_ntfy import send_ntfy_nfy

# 引入错误内容
from app.api.controller.ctrl_error import CustomHTTPException

# 推送消息到rabbit
async def push_msg_queue(chnl_id:str, tmpl_id: str, msg_list: List[dict]) -> str:

    try:
        chnl_ins = await NfyChnl.get(chnl_id=chnl_id)
        tmpl_ins = await NfyTmpl.get(tmpl_id=tmpl_id)

        rb_chnl_ins = await create_rb_channel()
        
        await rb_chnl_ins.declare_queue(name = chnl_ins.chnl_id, durable = True)
        
        # 定义表头
        msg_headers = {
            'chnl_type': chnl_ins.chnl_type,
            'chnl_auth_data': chnl_ins.chnl_auth_data,
            'tmpl_id': tmpl_ins.tmpl_id,
            'tmpl_args': tmpl_ins.tmpl_args
        }
        # 定义其他属性
        msg_properties = {
            'app_id': 'nfy_server',
            'content_type': 'application/json',
            'delivery_mode':2
        }

        for msg_data in msg_list:

            msg_body = json.dumps(msg_data).encode('utf-8')
            msg_ins = Message(headers= msg_headers, body=msg_body, **msg_properties)
            
            await rb_chnl_ins.default_exchange.publish(
                msg_ins, routing_key = chnl_ins.chnl_id
            )


    except Exception as e:

        print(str(e))
        raise CustomHTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = '频道模板错误',
            err_code = 13001
        )
    
    finally:

        await rb_chnl_ins.close()

    return 'success'
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

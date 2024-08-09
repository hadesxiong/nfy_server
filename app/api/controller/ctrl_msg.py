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
async def push_msg_queue(
        chnl_id:str,tmpl_id: str, 
        msg_list: List[dict]) -> str:

    print(chnl_id,tmpl_id,msg_list)

    try:
        chnl_ins = await NfyChnl.get(chnl_id=chnl_id)
        tmpl_ins = await NfyTmpl.get(tmpl_id=tmpl_id)

        rb_chnl_ins = await create_rb_channel()
        
        await rb_chnl_ins.declare_queue(
            name = chnl_ins.chnl_name,
            durable = True
        )

        for msg_data in msg_list:

            pass


    except Exception as e:

        print(str(e))
        raise CustomHTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = '频道模板错误',
            err_code = 13001
        )

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
    
# 从rabbit消费消息
async def process_msg(
    msg: Message) -> None:

    try:
        msg_data = msg.body.decode('utf-8')
        print(f'received message: {msg_data}')

    finally:
        await msg.ack()


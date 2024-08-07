# coding=utf8
import json
from typing import List
from aio_pika import RobustChannel, Message
from app.core.rabbit import create_rb_channel

# 推送消息到rabbit
async def push_msg_queue(
        chnl_name: str, 
        queue_name: str, 
        msg_list: List[dict]) -> str:
    # 使用 create_rb_channel 获取通道实例，并自动管理其生命周期
    chnl_ins = await create_rb_channel(chnl_name)
    try:
        await chnl_ins.declare_queue(name=queue_name, durable=True)
        for msg_data in msg_list:
            msg_body = json.dumps(msg_data).encode('utf-8')
            msg_ins = Message(body=msg_body)
            await chnl_ins.default_exchange.publish(
                msg_ins, routing_key=queue_name)
    finally:
        # 确保通道被关闭
        await chnl_ins.close()
    return 'success'
    
# 从rabbit消费消息
async def process_msg(
    msg: Message) -> None:

    try:
        msg_data = msg.body.decode('utf-8')
        print(f'received message: {msg_data}')

    finally:
        await msg.ack()


# coding=utf8
import asyncio
from typing import List, Callable, Any
from aio_pika import Message
from app.core.rabbit import create_rb_channel

# 定义消费函数
async def push_notify(msg:Message) -> None:

    try:
        msg_data = msg.body.decode('utf-8')
        print(msg_data)

    finally:
        await msg.ack()

async def start_consumer(
        chnl_list:List[str,Any],
        on_msg_callback: Callable[[Message,None]]) -> None:

    chnl_ins = await create_rb_channel()

    for each_chnl in chnl_list:
        queue_ins = await chnl_ins.declare_queue(name=each_chnl,durable=True)
        await queue_ins.consume(on_msg_callback)
    
    # print(f" [*] Waiting for messages in {}. To exit press CTRL+C")
    print(f"[*] Waiting for messages in. To exit press CTRL+C")

    try:

        # await chnl_ins.loop()
        pass

    except asyncio.CancelledError:

        print('closing consumer...')
        await queue_ins.cancel()
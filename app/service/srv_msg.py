# coding=utf8
import asyncio
from aio_pika import Message
from app.core.rabbit import create_rb_channel
from app.api.controller.ctrl_msg import process_msg

async def start_consumer(queue_name:str) -> None:

    chnl_ins = await create_rb_channel()
    
    queue_ins = await chnl_ins.declare_queue(name=queue_name,durable=True)
    async def on_msg(msg:Message) -> None:
        print(msg)
        await process_msg(msg)

    await queue_ins.consume(on_msg)

    print(f" [*] Waiting for messages in {queue_name}. To exit press CTRL+C")

    try:

        # await chnl_ins.loop()
        pass

    except asyncio.CancelledError:

        print('closing consumer...')
        await queue_ins.cancel()
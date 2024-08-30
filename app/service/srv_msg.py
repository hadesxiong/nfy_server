# coding=utf8
import asyncio,json
from typing import List, Callable, Any
from aio_pika import Message
from bson import ObjectId
# 引入方法
from app.service.srv_bark import send_bark_nfy
# 引入服务
from app.core.rabbit import create_rb_channel

# 定义消息推送函数用于被消费函数消费
async def push_notify(msg:Message) -> None:

    try:
        msg_data = json.loads(msg.body.decode('utf-8'))

        if msg.headers['chnl_type'] == 1:

            bark_kwargs = {
                'auth_user': msg.headers['chnl_auth_data']['auth_user'],
                'auth_pwd': msg.headers['chnl_auth_data']['auth_pwd'],
                'chnl_host': msg.headers['chnl_host'],
                'device_key': msg_data['receive']['device'],
                'usr_key': msg_data['receive']['key'],
                'usr_iv': msg_data['receive']['iv'],
                'title': msg.headers['tmpl_title'],
                'icon': msg.headers['tmpl_args']['tmpl_icon'],
                'body': msg.headers['tmpl_args']['tmpl_body'].format(**msg_data['detail']) 
            }

            send_rslt  = send_bark_nfy(**bark_kwargs)

            print(send_rslt)
            rec_data = {
                'rec_id': f'rec_{ObjectId()}',
                'tmpl_id': msg.headers['tmpl_id'],
                'rec_use': msg.app_id,
                'call_from': msg.app_id,
                'rec_data': bark_kwargs['body'],
                'rec_res': send_rslt,
                'rec_code': send_rslt,
                'rec_rcv': msg_data['receive']['id'],
                'rec_batch': msg_data['tmpl_id']
            }

            print(rec_data)

    finally:
        await msg.ack()


# 定义消费函数
async def start_consumer(
        chnl_list:List[str],
        on_msg_callback: Callable[[Message,None],None]) -> None:

    chnl_ins = await create_rb_channel()
    queue = []

    for each_chnl in chnl_list:
        queue_ins = await chnl_ins.declare_queue(name=each_chnl,durable=True)
        queue.append(queue_ins)
        await queue_ins.consume(on_msg_callback)
    
    # print(f" [*] Waiting for messages in {}. To exit press CTRL+C")
    print(f"[*] Waiting for messages in. To exit press CTRL+C")

    try:

        # await chnl_ins.loop()
        pass

    except asyncio.CancelledError:

        print('closing consumer...')
        for each in queue:
            await each.cancel()
# coding=utf8
import asyncio, aio_pika
from app.core.config import settings

# 创建链接
async def create_rb_connection() -> aio_pika.Connection:

    amqp_url = (
        f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PWD}@'
        f'{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}'
    )
    return await aio_pika.connect(amqp_url)


# 创建频道
async def create_rb_channel() -> aio_pika.Channel:
    # 确保 create_rb_connection 被 await 了，返回一个连接实例
    con_target = await create_rb_connection()
    # 使用通道实例作为上下文管理器
    chnl_target = await con_target.channel()
    return chnl_target
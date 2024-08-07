# coding=utf8
from tortoise import Tortoise

# 引入配置文件
from app.core.config import settings

modules = {'models':[
    'app.models.common',
    'app.models.receiver',
    'app.models.notify',
    'app.models.token'
]}

tortoise_cfg = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials":{
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "user": settings.DB_USERNAME,
                "password": settings.DB_PASSWORD,
                "database": settings.DB_NAME,
                "schema": settings.DB_SCHEMA
            }
        }
    },
    "apps": {
        "models": {
            "models": modules.get("models", []) + ["aerich.models"],
            "default_connection": "default"
        }
    }
}

async def init_db():
    await Tortoise.init(db_url=tortoise_cfg, modules=modules)

async def migrate_db():
    await init_db()
    await Tortoise.generate_schemas(safe=True)
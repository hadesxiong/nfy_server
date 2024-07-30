# coding=utf8
import os
from dotenv import load_dotenv

from tortoise import Tortoise

# 引入配置文件
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
env_path = os.path.join(target_dir, '.env')

load_dotenv(env_path)

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
                "host": os.getenv('DB_HOST'),
                "port": os.getenv('DB_PORT'),
                "user": os.getenv('DB_USERNAME'),
                "password": os.getenv('DB_PASSWORD'),
                "database": os.getenv('DB_NAME'),
                "schema": os.getenv('DB_SCHEMA')
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
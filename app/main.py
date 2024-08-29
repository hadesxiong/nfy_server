from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.core.config import settings

import app.core.db as db_base
from tortoise.contrib.fastapi import register_tortoise

from fastapi_pagination import add_pagination

from app.api.routers import *

from app.api.controller.ctrl_error import add_exception_handlers

from app.api.controller.ctrl_msg import get_chnl_list

from app.service.srv_msg import start_consumer,push_notify

@asynccontextmanager
async def lifespan(app:FastAPI):

    chnl_list = await get_chnl_list()
    await start_consumer(chnl_list,push_notify)
    yield


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME,lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

app.include_router(user_rt)
app.include_router(config_rt)
app.include_router(msg_rt)

register_tortoise(
    app,
    config = db_base.tortoise_cfg,
    modules = db_base.modules,
    generate_schemas=True,
    add_exception_handlers=True
)

add_pagination(app)
add_exception_handlers(app)

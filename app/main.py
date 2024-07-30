from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

import app.database.base as db_base
from tortoise.contrib.fastapi import register_tortoise


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

register_tortoise(
    app,
    db_url = db_base.db_url,
    modules = db_base.modules,
    generate_schemas=True,
    add_exception_handlers=True
)
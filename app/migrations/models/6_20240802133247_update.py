from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "nfy_pwd_auth";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ;"""

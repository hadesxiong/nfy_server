from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "nfy_token_detail";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ;"""

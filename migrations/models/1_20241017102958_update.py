from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_dict_mark" RENAME COLUMN "marK_stu" TO "mark_stu";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_dict_mark" RENAME COLUMN "mark_stu" TO "marK_stu";"""

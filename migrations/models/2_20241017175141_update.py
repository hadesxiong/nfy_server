from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_dict_mark" ALTER COLUMN "mark_ext_data" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_dict_mark" ALTER COLUMN "mark_ext_data" SET NOT NULL;"""

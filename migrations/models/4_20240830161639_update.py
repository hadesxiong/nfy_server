from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rcv_bark" ALTER COLUMN "bark_ext_data" DROP NOT NULL;
        ALTER TABLE "nfy_rcv_main" ALTER COLUMN "rcv_ext_data" DROP NOT NULL;
        ALTER TABLE "nfy_rcv_ntfy" ALTER COLUMN "ntfy_ext_data" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rcv_bark" ALTER COLUMN "bark_ext_data" SET NOT NULL;
        ALTER TABLE "nfy_rcv_main" ALTER COLUMN "rcv_ext_data" SET NOT NULL;
        ALTER TABLE "nfy_rcv_ntfy" ALTER COLUMN "ntfy_ext_data" SET NOT NULL;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_code" TYPE INT USING "rec_code"::INT;
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_res" TYPE VARCHAR(12) USING "rec_res"::VARCHAR(12);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_code" TYPE VARCHAR(12) USING "rec_code"::VARCHAR(12);
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_res" TYPE INT USING "rec_res"::INT;"""

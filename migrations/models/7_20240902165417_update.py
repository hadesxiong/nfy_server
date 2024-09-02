from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_use" DROP DEFAULT;
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_use" TYPE VARCHAR(64) USING "rec_use"::VARCHAR(64);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_use" TYPE INT USING "rec_use"::INT;
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_use" SET DEFAULT 1;"""

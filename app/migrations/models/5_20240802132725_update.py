from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_pwd_auth" ADD "usr_name" VARCHAR(64) NOT NULL;
        ALTER TABLE "nfy_usr_main" ALTER COLUMN "usr_ext_data" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_pwd_auth" DROP COLUMN "usr_name";
        ALTER TABLE "nfy_usr_main" ALTER COLUMN "usr_ext_data" SET NOT NULL;"""

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "nfy_pwd_auth" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL UNIQUE,
    "usr_name" VARCHAR(64) NOT NULL,
    "usr_pwd" VARCHAR(255) NOT NULL,
    "auth_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "auth_ext_data" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "nfy_pwd_auth";"""

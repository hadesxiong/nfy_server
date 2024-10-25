from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_nfy_dict_ma_mark_in_7b0ff8" ON "nfy_dict_mark" ("mark_index", "mark_value", "mark_abbr");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_nfy_dict_ma_mark_in_7b0ff8";"""

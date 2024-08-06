from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_chnl_main" ALTER COLUMN "chnl_ext_data" DROP NOT NULL;
        ALTER TABLE "nfy_chnl_main" ALTER COLUMN "chnl_auth_data" DROP NOT NULL;
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_ext_data" DROP NOT NULL;
        ALTER TABLE "nfy_tmpl_main" ALTER COLUMN "tmpl_args" DROP NOT NULL;
        ALTER TABLE "nfy_tmpl_main" ALTER COLUMN "tmpl_ext_data" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "nfy_rec_main" ALTER COLUMN "rec_ext_data" SET NOT NULL;
        ALTER TABLE "nfy_chnl_main" ALTER COLUMN "chnl_ext_data" SET NOT NULL;
        ALTER TABLE "nfy_chnl_main" ALTER COLUMN "chnl_auth_data" SET NOT NULL;
        ALTER TABLE "nfy_tmpl_main" ALTER COLUMN "tmpl_args" SET NOT NULL;
        ALTER TABLE "nfy_tmpl_main" ALTER COLUMN "tmpl_ext_data" SET NOT NULL;"""

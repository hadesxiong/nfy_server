from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "nfy_dict_mark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mark_id" VARCHAR(32) NOT NULL UNIQUE,
    "mark_index" VARCHAR(128) NOT NULL,
    "mark_code" INT NOT NULL,
    "mark_value" VARCHAR(128) NOT NULL,
    "marK_stu" INT NOT NULL,
    "mark_abbr" VARCHAR(128) NOT NULL,
    "mark_ext_data" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "nfy_pwd_auth" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL UNIQUE,
    "usr_name" VARCHAR(64) NOT NULL UNIQUE,
    "usr_pwd" VARCHAR(255) NOT NULL,
    "auth_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "auth_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_usr_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL UNIQUE,
    "usr_name" VARCHAR(64) NOT NULL UNIQUE,
    "usr_avatar" TEXT,
    "usr_role" INT NOT NULL  DEFAULT 1,
    "usr_stu" INT NOT NULL  DEFAULT 1,
    "usr_auth_type" INT NOT NULL,
    "usr_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "usr_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_group_detail" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_id" VARCHAR(32) NOT NULL,
    "group_rcv" VARCHAR(32) NOT NULL,
    "detail_stu" INT NOT NULL  DEFAULT 1,
    "detail_create_usr" VARCHAR(64) NOT NULL,
    "detail_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "detail_update_usr" VARCHAR(64) NOT NULL,
    "detail_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "detail_ext_data" JSONB,
    CONSTRAINT "uid_nfy_group_d_group_i_0aa333" UNIQUE ("group_id", "group_rcv", "detail_stu")
);
CREATE TABLE IF NOT EXISTS "nfy_rcv_bark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rcv_id" VARCHAR(32) NOT NULL UNIQUE,
    "device_key" VARCHAR(128) NOT NULL,
    "rcv_key" VARCHAR(128) NOT NULL,
    "rcv_iv" VARCHAR(128) NOT NULL,
    "bark_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_rcv_group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "group_id" VARCHAR(32) NOT NULL,
    "group_name" VARCHAR(128) NOT NULL,
    "group_type" INT NOT NULL  DEFAULT 1,
    "group_stu" INT NOT NULL  DEFAULT 1,
    "group_create_usr" VARCHAR(64) NOT NULL,
    "group_update_usr" VARCHAR(64) NOT NULL,
    "group_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "group_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "group_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_rcv_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rcv_id" VARCHAR(32) NOT NULL UNIQUE,
    "rcv_chnl" VARCHAR(128) NOT NULL,
    "rcv_stu" INT NOT NULL  DEFAULT 1,
    "rcv_type" INT NOT NULL  DEFAULT 1,
    "rcv_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "rcv_create_usr" VARCHAR(32) NOT NULL,
    "rcv_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "rcv_update_usr" VARCHAR(32) NOT NULL,
    "rcv_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_rcv_ntfy" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rcv_id" VARCHAR(32) NOT NULL UNIQUE,
    "rcv_name" VARCHAR(128) NOT NULL,
    "rcv_role" INT NOT NULL  DEFAULT 1,
    "rcv_topic" VARCHAR(255) NOT NULL,
    "rcv_perm" INT NOT NULL  DEFAULT 1,
    "ntfy_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_chnl_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chnl_id" VARCHAR(32) NOT NULL UNIQUE,
    "chnl_name" VARCHAR(128) NOT NULL,
    "chnl_type" INT NOT NULL  DEFAULT 1,
    "chnl_stu" INT NOT NULL  DEFAULT 1,
    "chnl_host" VARCHAR(255) NOT NULL,
    "chnl_auth_method" INT NOT NULL  DEFAULT 1,
    "chnl_auth_data" JSONB,
    "chnl_create_usr" VARCHAR(32) NOT NULL,
    "chnl_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "chnl_update_usr" VARCHAR(32) NOT NULL,
    "chnl_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "chnl_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_rec_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rec_id" VARCHAR(32) NOT NULL UNIQUE,
    "tmpl_id" VARCHAR(32) NOT NULL,
    "rec_use" VARCHAR(64) NOT NULL,
    "call_from" VARCHAR(128) NOT NULL,
    "rec_data" JSONB,
    "rec_code" INT NOT NULL,
    "rec_res" VARCHAR(12) NOT NULL,
    "rec_msg" TEXT NOT NULL,
    "rec_rcv" VARCHAR(32) NOT NULL,
    "rec_batch" VARCHAR(64) NOT NULL,
    "rec_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_tmpl_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tmpl_id" VARCHAR(32) NOT NULL UNIQUE,
    "tmpl_chnl" VARCHAR(32) NOT NULL,
    "tmpl_title" VARCHAR(255) NOT NULL,
    "tmpl_stu" INT NOT NULL  DEFAULT 1,
    "tmpl_args" JSONB,
    "tmpl_create_usr" VARCHAR(32) NOT NULL,
    "tmpl_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "tmpl_update_usr" VARCHAR(32) NOT NULL,
    "tmpl_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "tmpl_ext_data" JSONB
);
CREATE TABLE IF NOT EXISTS "nfy_token_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL,
    "usr_aid" VARCHAR(128) NOT NULL UNIQUE,
    "usr_secret" VARCHAR(128) NOT NULL UNIQUE,
    "secret_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

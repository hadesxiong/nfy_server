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
    "usr_pwd" VARCHAR(255) NOT NULL,
    "auth_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "auth_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_usr_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL UNIQUE,
    "usr_name" VARCHAR(64) NOT NULL,
    "usr_avatar" TEXT,
    "usr_role" INT NOT NULL  DEFAULT 1,
    "usr_stu" INT NOT NULL  DEFAULT 1,
    "usr_auth_type" INT NOT NULL,
    "usr_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "usr_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_rcv_bark" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rcv_id" VARCHAR(32) NOT NULL UNIQUE,
    "device_key" VARCHAR(128) NOT NULL,
    "rcv_key" VARCHAR(128) NOT NULL,
    "rcv_iv" VARCHAR(128) NOT NULL,
    "bark_ext_data" JSONB NOT NULL
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
    "rcv_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_rcv_ntfy" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rcv_id" VARCHAR(32) NOT NULL UNIQUE,
    "rcv_name" VARCHAR(128) NOT NULL,
    "rcv_role" INT NOT NULL  DEFAULT 1,
    "rcv_topic" VARCHAR(255) NOT NULL,
    "rcv_perm" INT NOT NULL  DEFAULT 1,
    "ntfy_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_chnl_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chnl_id" VARCHAR(32) NOT NULL UNIQUE,
    "chnl_name" VARCHAR(128) NOT NULL,
    "chnl_type" INT NOT NULL  DEFAULT 1,
    "chnl_stu" INT NOT NULL  DEFAULT 1,
    "chnl_host" VARCHAR(255) NOT NULL,
    "chnl_auth_method" INT NOT NULL  DEFAULT 1,
    "chnl_auth_data" JSONB NOT NULL,
    "chnl_create_usr" VARCHAR(32) NOT NULL,
    "chnl_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "chnl_update_usr" VARCHAR(32) NOT NULL,
    "chnl_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "chnl_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_rec_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rec_id" VARCHAR(32) NOT NULL UNIQUE,
    "tmpl_id" VARCHAR(32) NOT NULL,
    "rec_use" INT NOT NULL  DEFAULT 1,
    "call_from" VARCHAR(128) NOT NULL,
    "rec_data" JSONB NOT NULL,
    "rec_res" INT NOT NULL,
    "rec_code" VARCHAR(12) NOT NULL,
    "rec_msg" TEXT NOT NULL,
    "rec_rcv" VARCHAR(32) NOT NULL,
    "rec_batch" VARCHAR(64) NOT NULL,
    "rec_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_tmpl_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "tmpl_id" VARCHAR(32) NOT NULL UNIQUE,
    "tmpl_chnl" VARCHAR(32) NOT NULL,
    "tmpl_title" VARCHAR(255) NOT NULL,
    "tmpl_stu" INT NOT NULL  DEFAULT 1,
    "tmpl_args" JSONB NOT NULL,
    "tmpl_create_usr" VARCHAR(32) NOT NULL,
    "tmpl_create_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "tmpl_update_usr" VARCHAR(32) NOT NULL,
    "tmpl_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "tmpl_ext_data" JSONB NOT NULL
);
        CREATE TABLE IF NOT EXISTS "nfy_token_detail" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token_id" VARCHAR(32) NOT NULL UNIQUE,
    "usr_id" VARCHAR(32) NOT NULL,
    "usr_token" VARCHAR(128) NOT NULL,
    "token_expire" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "nfy_token_main" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "usr_id" VARCHAR(32) NOT NULL,
    "usr_aid" VARCHAR(128) NOT NULL UNIQUE,
    "usr_secret" VARCHAR(128) NOT NULL UNIQUE,
    "secret_update_dt" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "nfy_dict_mark";
        DROP TABLE IF EXISTS "nfy_pwd_auth";
        DROP TABLE IF EXISTS "nfy_usr_main";
        DROP TABLE IF EXISTS "nfy_rcv_bark";
        DROP TABLE IF EXISTS "nfy_rcv_main";
        DROP TABLE IF EXISTS "nfy_rcv_ntfy";
        DROP TABLE IF EXISTS "nfy_chnl_main";
        DROP TABLE IF EXISTS "nfy_rec_main";
        DROP TABLE IF EXISTS "nfy_tmpl_main";
        DROP TABLE IF EXISTS "nfy_token_detail";
        DROP TABLE IF EXISTS "nfy_token_main";"""

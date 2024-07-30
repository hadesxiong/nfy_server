# coding=utf8
from pydantic import BaseModel, Field
from datetime import datetime

from typing import List

from api.schema.basic import ResBasic

# 定义基本模型
# 查询基本模型

class UserInfoQuery(BaseModel):

    usr_id: str | None = Field(default=None,alias='id')
    usr_name: str | None = Field(default=None,alias='name')
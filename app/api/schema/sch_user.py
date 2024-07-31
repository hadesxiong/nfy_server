# coding=utf8
from pydantic import BaseModel, Field
from datetime import datetime

from typing import List

from app.api.schema.basic import ResBasic

# 定义基本模型
# Request模型
class UserInfoQuery(BaseModel):

    usr_id: str | None = Field(default=None,alias='id')
    usr_name: str | None = Field(default=None,alias='name')
    usr_stu: int | None = Field(default=None,alias='statu')
    usr_auth_type: int | None = Field(default=None,alias='auth')
    usr_create_dt__gte: str | None = Field(default=None,alias='start')
    usr_create_dt__lte: str | None = Field(default=None,alias='end')

    class Config:
        extra = 'forbid'


# Response模型
class UserInfoRst(BaseModel):

    usr_id: str | None = Field(default=None)
    usr_name: str | None = Field(default=None)
    usr_avatar: str | None = Field(default=None)
    usr_role: int | None = Field(default=None)
    usr_auth_type: int | None = Field(default=None)
    usr_create_dt: datetime | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class UserInfoRes(ResBasic):

    data: List[UserInfoRst] | None = Field(default=None)
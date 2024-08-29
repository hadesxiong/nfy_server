# coding=utf8
from pydantic import BaseModel,Field
from datetime import datetime
from typing import Dict,Any

from app.api.schema.basic import ResBasic

# 定义基本模型
# Request模型
class ChannelUpdateForm(BaseModel):

    chnl_name: str | None = Field(default=None,alias='name')
    chnl_type: int | None = Field(default=None,alias='type')
    chnl_stu: int | None = Field(default=None,alias='statu')
    chnl_host: str | None = Field(default=None,alias='host')
    chnl_auth_method: int | None = Field(default=None, alias='auth_type')
    chnl_auth_data: Dict[str,Any] | None = Field(default=None,alias='auth_data')
    chnl_ext_data: Dict[str,Any] | None = Field(default=None,alias='auth_ext')

    class Config:
        extra = 'forbid'

class ChannelUpdateQuery(ChannelUpdateForm):

    chnl_id: str | None = Field(default=None,alias='chnl')
    form: ChannelUpdateForm | None = Field(default=None,alias='data')

    class Config:
        extra = 'allow'

class TemplateUpdateForm(BaseModel):

    tmpl_title: str | None = Field(default=None,alias='title')
    tmpl_stu: int | None = Field(default=None, alias='statu')
    tmpl_chnl: str | None = Field(default=None, alias='channel')
    tmpl_args: Dict[str,Any] | None = Field(default=None, alias='args')
    tmpl_ext_data: Dict[str,Any] | None = Field(default=None, alias='tmpl_ext')

    class Config:
        extra = 'forbid'

class TemplateUpdateQuery(TemplateUpdateForm):
    tmpl_id: str | None = Field(default=None, alias='tmpl')
    form: TemplateUpdateForm | None  = Field(default=None, alias='data')

    class Config:
        extra = 'allow'

# Response模型
class UpdateRst(ResBasic):

    target: str | None = Field(default=None)
    dt: str | None = Field(default=None)

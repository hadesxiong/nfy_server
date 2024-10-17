# coding=utf8
import json
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Dict,Any,List

from app.api.schema.basic import ResBasic

# 定义基本模型
# Request模型
class DictQueryForm(BaseModel):

    mark_index: str | None = Field(default=None, alias='index')
    mark_code: int | None = Field(default=None, alias='code')
    mark_value: str | None = Field(default=None, alias='value')
    key_word: str | None = Field(default=None, alias='key')
    page_no: int | None = Field(default=1, alias='page')
    page_size: int | None = Field(default=10, alias='size')
    order_by: str | None = Field(default=None, alias='order')

    class Config:
        extra = 'forbid'

class DictUpdateForm(BaseModel):

    mark_index: str | None = Field(default=None, alias='index')
    mark_code: int | None = Field(default=None, alias='code')
    mark_value: str | None = Field(default=None, alias='value')
    mark_abbr: str | None = Field(default=None, alias='table')
    mark_stu: int | None = Field(default=1, alias='statu')

    class Config:
        extra = 'forbid'

class DictUpdate(DictUpdateForm):

    mark_id: str | None = Field(default=None, alias='dict')
    form: DictUpdateForm | None = Field(default=None, alias='data')

    @field_validator('form')
    def form_not_empty(cls,v):
        if not v:
            try:
                raise ValueError('dict_data cannot be empty')
            except ValueError as e:
                error_info = {
                    'type': '类型错误',
                    'msg': str(e)
                }
                return json.dumps(error_info)
        return v

class DictInfoRes(BaseModel):

    mark_id: str | None = Field(default=None)
    mark_index: str | None = Field(default=None)
    mark_code: int | None = Field(default=None)
    mark_value: str | None = Field(default=None)
    mark_abbr: str | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class DictListRes(DictInfoRes):

    data: List[DictInfoRes] | DictInfoRes | None = Field(default=None)
    page: int | None = Field(default=None)
    size: int | None = Field(default=None)
    total: int | None = Field(default=None)
    has_next: bool | None = Field(default=None)

class UpdateRst(ResBasic):

    target: str | Dict[str,Any] | None = Field(default=None)
    dt: str | None = Field(default=None)
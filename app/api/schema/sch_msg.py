# coding=utf8
import json
from pydantic import BaseModel, Field, field_validator
from typing import List,Dict,Any

from app.api.schema.basic import ResBasic

# 定义基本模型
# Request模型

class MsgData(BaseModel):

    msg_type: int = Field(default=1,alias='type')
    msg_rcv: str = Field(default='all', alias='receive')
    msg_target: str | None = Field(default=None,alias='target')
    msg_data: Dict[str,Any] = Field(alias='data')
    msg_url: str | None = Field(default=None, alias='link')
    msg_url_data: Dict[str,Any] | None = Field(default=None, alias='args')

    @field_validator('msg_data')
    def msg_data_not_empty(cls,v):
        if not v:
            try:
                raise ValueError('msg_data cannot be empty')
            except ValueError as e:
                error_info = {
                    'type': '类型错误',
                    'msg': str(e)
                }
                return json.dumps(error_info)
        return v

class MsgQueue(BaseModel):

    chnl_id: str = Field(alias='channel')
    tmpl_id: str = Field(alias='template')
    call_from: str = Field(alias='call')
    msg_dict: MsgData = Field(alias='message')

    @field_validator('msg_dict')
    def msg_list_not_empty(cls,v):
        if not v:
            try: 
                raise ValueError('msg_list must not be empty')
            except ValueError as e:
                error_info = {
                    'type': '类型错误',
                    'msg': str(e)
                }
                return json.dumps(error_info)
        return v

class MsgRecQuery(BaseModel):

    rec_id : str | None = Field(default=None,alias='record')
    tmpl_id: str | None = Field(default=None,alias='template')
    call_from: str | None = Field(default=None,alias='call')
    rec_code: int | None = Field(default=None,alias='code')
    rec_rcv: str | None = Field(default=None,alias='receiver')
    rec_batch: str | None = Field(default=None,alias='batch')
    key_word: str | None = Field(default=None,alias='key')
    page_no: int | None = Field(default=1,alias='page')
    page_size: int | None = Field(default=10,alias='size')
    order_by: str | None = Field(default=None,alias='order')

    class Config:

        extra = 'forbid'

# 定义回复模型
class MsgRes(ResBasic):

    receive_total_count: int | None = Field(default=None)
    template_title: str | None = Field(default=None)
    channel_type: int | None = Field(default=None)

class MsgRecRst(BaseModel):
    rec_id: str | None = Field(default=None)
    tmpl_id: str | None = Field(default=None)
    rec_use: str | None = Field(default=None)
    call_from: str | None = Field(default=None)
    rec_data: dict | None = Field(default=None)
    rec_code: int | None = Field(default=None)
    rec_res: str | None = Field(default=None)
    rec_msg: str | None = Field(default=None)
    rec_rcv: str | None = Field(default=None)
    rec_batch: str | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class MsgRecRes(MsgRecRst):

    data: MsgRecRst | List[MsgRecRst] | None = Field(default=None)
    page: int = Field(default=1)
    size: int = Field(default=10)
    total: int | None = Field(default=None)
    has_next: bool | None = Field(default=None)
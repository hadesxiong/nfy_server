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
    
# 定义回复模型
class MsgRes(ResBasic):

    receive_total_count: int | None = Field(default=None)
    template_title: str | None = Field(default=None)
    channel_type: int | None = Field(default=None)
# coding=utf8
from pydantic import BaseModel, Field, field_validator

from typing import List,Dict,Any

# 定义基本模型
# Request模型
class MsgQueue(BaseModel):

    chnl_id: str = Field(alias='channel')
    tmpl_id: str = Field(alias='template')
    msg_list: List[Dict[str,Any]] = Field(alias='data')

    @field_validator('msg_list')
    def msg_list_not_empty(cls,v):

        if not v: 
            raise ValueError('msg_list must not be empty')
        return v
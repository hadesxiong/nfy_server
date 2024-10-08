# coding=utf8
import json
from pydantic import BaseModel,Field,field_validator
from datetime import datetime
from typing import Dict,Any,List

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

class ChannelQueryForm(BaseModel):
    chnl_id: str | None = Field(default=None,alias='channel')
    chnl_type: int | None = Field(default=None, alias='type')
    start_dt: str | None = Field(default=None, alias='start')
    end_dt: str | None = Field(default=None, alias='end')
    key_word: str | None = Field(default=None, alias='key')
    page_no: int | None = Field(default=1,alias='page')
    page_size: int | None = Field(default=10,alias='size')
    order_by: str | None = Field(default=None,alias='order')

    class Config:
        extra = 'forbid'

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

class TemplateQueryForm(BaseModel):
    tmpl_id: str | None = Field(default=None,alias='template')
    tmpl_chnl: str | None = Field(default=None,alias='channel')
    start_dt: str | None = Field(default=None,alias='start')
    end_dt: str | None = Field(default=None,alias='end')
    key_word: str | None = Field(default=None, alias='key')
    page_no: int | None = Field(default=1,alias='page')
    page_size: int | None = Field(default=10,alias='size')
    order_by: str | None = Field(default=None,alias='order')

    class Config:
        extra = 'forbid'

class ReceiverBark(BaseModel):

    rcv_id: str | None = Field(default=None, alias='id')
    device_key: str | None = Field(default=None, alias='device')
    key: str | None = Field(default=None, alias='key')
    iv: str | None = Field(default=None, alias='iv')
    class Config:
        extra = 'forbid'

class ReceiverNtfy(BaseModel):

    rcv_id: str | None = Field(default=None, alias='id')
    rcv_name: str | None = Field(default=None, alias='name')
    rcv_role: int | None = Field(default=None, alias='role')
    rcv_topic: str | None = Field(default=None, alias='topic')
    rcv_perm: int | None = Field(default=None, alias='permission')

    class Config:
        extra = 'forbid'

class ReceiverUpdateForm(ReceiverBark,ReceiverNtfy):

    rcv_id: str | None = Field(default=None, alias='target')
    rcv_type: int | None = Field(default=None, alias='type')
    rcv_stu: int | None = Field(default=None, alias='statu')
    rcv_chnl: str | None = Field(default=None, alias='channel')
    form: ReceiverNtfy | ReceiverBark | None = Field(default=None, alias='data')

    @field_validator('form')
    def form_not_empty(cls,v):
        if not v:
            try:
                raise ValueError('rcv_data cannot be empty')
            except ValueError as e:
                error_info = {
                    'type': '类型错误',
                    'msg': str(e)
                }
                return json.dumps(error_info)
        return v
    
class ReceiverGroupUpdate(BaseModel):

    group_id: str | None = Field(default=None, alias='group')
    group_name: str | None = Field(default=None, alias='name')
    group_type: int | None = Field(default=None, alias='type')
    group_stu: int | None = Field(default=None, alias='statu')
    group_rcv: str | List[str] | None = Field(default=None, alias='receiver')

    class config:
        extra = 'forbid'

class ReceiverQueryForm(BaseModel):

    target_class: int = Field(default=1,alias='tar_class')
    target_id: str | None = Field(default=None,alias='target')
    group_name: str | None = Field(default=None,alias='name')
    rcv_chnl: str | None = Field(default=None,alias='channel')
    rcv_type: int | None = Field(default=None,alias='type')
    start_dt: str | None = Field(default=None,alias='start')
    end_dt: str | None = Field(default=None,alias='end')
    key_word: str | None = Field(default=None,alias='key')
    page_no: int | None = Field(default=1,alias='page')
    page_size: int | None = Field(default=10,alias='size')
    order_by: str | None = Field(default=None,alias='order')

    class Config:
        extra = 'forbid'

# Response模型
class UpdateRst(ResBasic):

    target: str | None = Field(default=None)
    dt: str | None = Field(default=None)

class ChannelInfoRst(BaseModel):

    chnl_id: str | None = Field(default=None)
    chnl_name: str | None = Field(default=None)
    chnl_type: int | None = Field(default=None)
    chnl_auth_method: int | None =Field(default=None)
    chnl_host: str | None = Field(default=None)
    chnl_update_dt: datetime | None = Field(default=None)
    chnl_update_usr: str | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class ChannelInfoRes(ChannelInfoRst):

    data: ChannelInfoRst | List[ChannelInfoRst] | None = Field(default=None)
    page: int = Field(default=1)
    size: int = Field(default=10)
    total: int | None = Field(default=None)
    has_next: bool | None = Field(default=None)

class TemplateInfoRst(BaseModel):

    tmpl_id: str | None = Field(default=None)
    tmpl_chnl: str | None = Field(default=None)
    tmpl_title: str | None = Field(default=None)
    tmpl_args: dict | None = Field(default=None)
    tmpl_update_usr: str | None = Field(default=None)
    tmpl_update_dt: datetime | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class TemplateInfoRes(TemplateInfoRst):

    data: TemplateInfoRst | List[TemplateInfoRst] | None = Field(default=None)
    page: int = Field(default=1)
    size: int = Field(default=10)
    total: int | None = Field(default=None)
    has_next: bool | None = Field(default=None)

class ReceiverInfoRst(BaseModel):

    rcv_id : str | None = Field(default=None)
    rcv_chnl: str | None = Field(default=None)
    rcv_type: int | None = Field(default=None)
    rcv_update_usr: str | None = Field(default=None)
    rcv_update_dt: datetime | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class RcvGroupInfoRst(BaseModel):

    group_id: str | None = Field(default=None)
    group_name: str | None = Field(default=None)
    group_type: int | None = Field(default=None)
    group_rcv: str | list | None = Field(default=None)
    group_update_usr: str | None = Field(default=None)
    group_update_dt: datetime | None = Field(default=None)

    class Config:

        extra = 'allow'
        from_attributes = True

class ReceiverListRes(ReceiverInfoRst,RcvGroupInfoRst):

    data: ReceiverInfoRst | List[ReceiverInfoRst] | \
        RcvGroupInfoRst | List[RcvGroupInfoRst] | \
        None = Field(default=None)
    page: int = Field(default=1)
    size: int = Field(default=10)
    total: int | None = Field(default=None)
    has_next: bool | None = Field(default=None)
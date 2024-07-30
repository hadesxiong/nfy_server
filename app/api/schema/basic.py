# coding=utf8
from pydantic import BaseModel,Field

# 定义基本回复模型
class ResBasic(BaseModel):

    code: int | None = Field(default=200)
    msg: str | None = Field(default='success')
    error: str | None = Field(default=None)
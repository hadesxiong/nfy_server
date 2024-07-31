# coding=utf8
from tortoise.expressions import Q
from app.models.common import UserMain

from app.utils.query import build_query_exp

async def get_userinfo_handler(filters):
    print(filters)
    filters_list = [{'key':k,'value':v} for k,v in filters.items()]
    print(build_query_exp(filters_list))

    filter_query = build_query_exp(filters_list)

    user_rslt = await UserMain.filter(filter_query)

    return user_rslt
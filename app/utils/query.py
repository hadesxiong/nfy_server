# coding=utf8
from typing import List, Dict, Any
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

def build_query_exp(filters:Dict[str,Any],logics:Dict[str,Any]=None) -> Any:

    '''
    入参定义：
    fitlers: 通过request模型形成的字典,key:value类型,其中key指代数据库字段,value指代目标筛选值
    logics: 定义好的针对filters中可能出现的逻辑方法,key:logic,其中key与filters中保持一致,logic代表tortoise的逻辑运算法后缀
    通过组装filters+logics来形成query表达式
    '''
    rslt_query = Q()
    fltr_list = []
    for key,value in filters.items():
        # 检查 logics 是否为 None 或者 key 是否不在 logics 中
        if logics is None or key not in logics:
            fltr_list.append({'key': key, 'value': value})
        else:
            fltr_list.append({'key': key, 'value': value, 'logic': logics[key]})

    # 遍历表达式子项进行拼接
    for each_filter in fltr_list:
        
        if each_filter.get('key') is None or each_filter.get('value') is None:
            continue
        
        key,value,logic = each_filter['key'], each_filter['value'], each_filter.get('logic')
        query_key = f'{key}__{logic}' if logic and logic != 'equal' else key

        rslt_query &= Q(**{query_key:value})
    
    return rslt_query

def build_or_exp(keys:List[str],value:Any) -> Any:

    rslt_query = Q()

    for each_key in keys:

        rslt_query |= Q(**{f'{each_key}__icontains':value})

    return rslt_query

async def distinct_query(queryset,*fields):

    '''
    对Tortoise-orm的queryset进行去重

    :param queryset: 需要去重的queryset对象
    :param fields: 依据去重的字段名称
    :return: 去重后的模型对象
    '''

    items = await queryset.all()

    # 创建一个字典用于存储去重后的对象
    unique_items = {}

    for item in items:

        # 创建一个元组，包含所有需要去重的字段的值
        key = tuple(getattr(item,field) for field in fields)
        if key not in unique_items:
            unique_items[key] = item

    # 返回去重后的模型对象列表
    return list(unique_items.values())

async def paginate_query(items,page,size):

    '''
    对列表进行分页，并返回分页信息。

    :param items: 模型对象列表。
    :param page: 当前页码。
    :param size: 每页大小。
    :return: 分页后的结果和分页信息。
    '''

    total = len(items)
    page = int(page)
    size = int(size)
    offset = (page - 1) * size
    items_page = items[offset:offset + size]
    pages = (total + size - 1) // size  # 计算总页数，向上取整
    
    return {'items': items_page,'total': total,
            'page': page,'size': size,'pages': pages}
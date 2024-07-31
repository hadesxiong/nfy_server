# coding=utf8
from typing import List, Dict, Any
from tortoise.expressions import Q

def build_query_exp(filters:Dict[str,Any],logics:Dict[str,Any]=None) -> Any:

    '''
    入参定义：
    fitlers: 通过request模型形成的字典,key:value类型，其中key指代数据库字段，value指代目标筛选值
    logics: 定义好的针对filters中可能出现的逻辑方法,key:logic，其中key与filters中保持一致,logic代表tortoise的逻辑运算法后缀
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


    for each_filter in fltr_list:
        
        if each_filter.get('key') is None or each_filter.get('value') is None:
            continue
        
        key,value,logic = each_filter['key'], each_filter['value'], each_filter.get('logic')
        query_key = f'{key}__{logic}' if logic and logic != 'equal' else key

        rslt_query &= Q(**{query_key:value})
    
    return rslt_query
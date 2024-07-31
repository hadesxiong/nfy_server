# coding=utf8
from typing import List, Dict, Any
from tortoise.expressions import Q

def build_query_exp(filters: List[Dict[str,Any]]) -> Any:

    # 理论上通过传入key,value,logic来组成查询函数
    rslt_query = Q()
    
    for each_filter in filters:
        
        if each_filter.get('key') is None or each_filter.get('value') is None:
            continue
        
        key,value,logic = each_filter['key'], each_filter['value'], each_filter.get('logic')
        query_key = f'{key}__{logic}' if logic and logic != 'equal' else key

        rslt_query &= Q(**{query_key:value})
    
    return rslt_query
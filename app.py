import importlib
import json
import logging

from cmdb.types import Int, get_instance, inject_classes_cache
from cmdb.utils import getlogger

jsonstr = """
{
    "type":"cmdb.types.IP",
    "value":"172.1.0.1",
    "option":{
        "prefix":"172.1"
    }
    
}
"""

obj = json.loads(jsonstr)
print(obj)

inject_classes_cache() # 函数调用放在模块后面

print(get_instance(obj['type'],**obj['option']).stringify(obj['value']))
print(get_instance(obj['type'],**obj['option']).stringify(obj['value']))

def a ():
    logger = getlogger(__name__, '/Users/quyixiao/ttg/test.log')  # 路径自行更换
    logger.info('...................xxxxxxxxxxxxxxxxxxx')


a()
import importlib
import json

from cmdb.types import Int, get_instance

jsonstr = """
{
    "type":"cmdb.types.Int",
    "value":300
}
"""

obj = json.loads(jsonstr)
print(obj)

print(get_instance(obj['type']).stringify(obj['value']))

import importlib
import ipaddress

# 使用反射实现动态加载类型方式，非常的灵活，可以扩展更多的类型，并把数据验证，转换北外乡类型自己完成
# 这是一种插件化的编程思想具体的实现
#
def get_instance(type: str):
    m, c = type.rsplit('.', maxsplit=1)
    mod = importlib.import_module(m)
    cls = getattr(mod, c)
    obj = cls()
    if isinstance(obj, BaseType):
        return obj
    return TypeError('Wrong Type! {} is not sub class of BaseType'.format(type))


class BaseType:
    def stringify(self, value):
        raise NotImplementedError()

    def destringify(self, value):
        raise NotImplementedError()


class Int(BaseType):
    def stringify(self, value):
        return str(int(value))

    def destringify(self, value):
        return value


class IP(BaseType):
    def stringify(self, value):
        return str(ipaddress.ip_address(value))

    def destringify(self, value):
        return value

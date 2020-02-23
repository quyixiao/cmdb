import importlib
import ipaddress

# 使用反射实现动态加载类型方式，非常的灵活，可以扩展更多的类型，并把数据验证，转换北外乡类型自己完成
# 这是一种插件化的编程思想具体的实现
#

classes_cache = {}  # 类缓存
instances_cache = {}  # 实例缓存


def inject_classes_cache():
    mod = globals().get('__package__')
    for k, v in globals().items():
        if type(v) == type and k != 'BaseType' and issubclass(v, BaseType):
            classes_cache[k] = v
            classes_cache[".".join((mod, k))] = v


def get_class(type: str):
    # 使用缓存
    cls = classes_cache.get(type)
    if cls:
        return cls
    m, c = type.rsplit('.', maxsplit=1)
    mod = importlib.import_module(m)
    cls = getattr(mod, c)
    if issubclass(cls, BaseType):
        classes_cache[type] = cls
        return cls
    return TypeError('Wrong Type! {} is not sub class of BaseType'.format(type))


def get_instance(type: str, **option):
    key = ",".join("{}={}".format(k, v) for k, v in sorted(option.items()))
    key = "{}|{}".format(type, key)
    instance = instances_cache.get(key)
    if instance:
        return instance
    cls = get_class(type)
    instance = cls(**option)
    instances_cache[key] = instance
    return instance


class BaseType:
    def __init__(self, **option):
        self.__dict__['option'] = option

    def __getattr__(self, item):
        return self.option.get(item)

    def stringify(self, value):
        raise NotImplementedError()

    def destringify(self, value):
        raise NotImplementedError()


class Int(BaseType):
    def stringify(self, value):
        val = int(value)
        max = self.max
        min = self.min
        if max and val > max:
            raise ValueError('值过大，大于最大值 {} '.format(max))
        elif min and val < min:
            raise ValueError('值过小，小于最小值 {} '.format(min))
        return str(val)

    def destringify(self, value):
        return value


class IP(BaseType):
    '''实现IP数据校验和转换'''

    def stringify(self, value):
        """转换，错误的数据不要给默认值，就抛异常让外部捕获"""
        prefix = self.prefix
        if prefix and not str(value).startswith(prefix):
            raise ValueError('Must start with {}'.format(prefix))

        return str(ipaddress.ip_address(value))

    def destringify(self, value):
        return value

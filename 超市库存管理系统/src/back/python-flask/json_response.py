# 统一的json返回格式

class JsonResponse(object):

    # __init__是一个特殊方法用于在创建对象时进行初始化操作
    # 通过这个方法可以为JsonResponse对象绑定code、msg和data属性
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    # @classmethod修饰符对应的函数不需要实例化，不需要 self 参数，
    # 但第一个参数需要是表示自身类的 cls 参数，可以来调用类的属性，类的方法，实例化对象等
    @classmethod
    def success(cls, code=200, msg='success', data=None):
        return cls(code, msg, data)

    @classmethod
    def fail(cls, code=400, msg='fail', data=None):
        return cls(code, msg, data)

    # 定义返回json对象方法
    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }


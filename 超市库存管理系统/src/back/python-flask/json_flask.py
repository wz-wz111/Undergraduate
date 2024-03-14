from flask import Flask, jsonify

from json_response import JsonResponse

# Flask视图函数默认是不能返回list对象和None的，如果返回数据不对，就会抛出异常
# 将Flask改造为视图函数返回支持list、dict、None
class JsonFlask(Flask):
    def make_response(self, rv):
        # isinstance() 函数来判断一个对象是否是一个已知的类型，会考虑继承关系
        if rv is None or isinstance(rv, (list, dict)):
            rv = JsonResponse.success(rv)

        if isinstance(rv, JsonResponse):
            # 将数据序列化为JSON并将其封装在flask中
            rv = jsonify(rv.to_dict())

        # 将返回值从一个视图函数转换为response_class的实例
        return super().make_response(rv)


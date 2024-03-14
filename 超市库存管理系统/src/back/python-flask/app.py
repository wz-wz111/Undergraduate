from flask import request
from flask_cors import *

from json_flask import JsonFlask
from json_response import JsonResponse
from db import *
from datetime import datetime
import json

# 创建视图应用，使用改造后的JsonFlask对象
app = JsonFlask(__name__)

# 解决跨域
CORS(app, supports_credentials=True)

# 数据库连接对象
db = SQLManager()


# 编写视图函数，绑定路由
# client表
@app.route("/all_client", methods=["GET"])  # 查询（全部）
def all_client():
    result = db.get_list(sql='select * from client')
    return JsonResponse.success(msg='查询成功', data=result)

@app.route("/add_client", methods=["POST"])  # 添加（单个）
def add_client():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into client(client_id,client_name,phone_number,address) values(%s,%s,%s,%s)',
                     args=[data['client_id'], data['client_name'], data['phone_number'], data['address']])
    # python三元表达式
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')

@app.route("/update_client", methods=["PUT"])  # 修改（单个）
def update_client():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'client_id' not in data:  # 改为form里对应的xx_id
        return JsonResponse.fail(msg='需要传入client_id')
    isOk = db.modify(sql='update client set client_name=%s,phone_number=%s,address=%s where client_id=%s',  # 改为
                     args=[data['client_name'], data['phone_number'], data['address'], data['client_id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='修改失败')


@app.route("/delete_client", methods=["DELETE"])  # 删除（单个）
def delete_client():
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'client_id' not in request.args:
        return JsonResponse.fail(msg='需要传入client_id')
    isOk = db.modify(sql='delete from client where client_id=%s', args=[request.args['client_id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')

# staff表
@app.route("/all_staff", methods=["GET"])  # 查询（全部）
def all_staff():
    result = db.get_list(sql='select * from staff')
    return JsonResponse.success(msg='查询成功', data=result)

@app.route("/add_staff", methods=["POST"])  # 添加（单个）
def add_staff():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into staff(staff_id,staff_name,department,salary,phone_number) values(%s,%s,%s,%s,%s)',
                     args=[data['staff_id'], data['staff_name'], data['department'], data['salary'],  data['phone_number']])
    # python三元表达式
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')

@app.route("/update_staff", methods=["PUT"])  # 修改（单个）
def update_staff():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'staff_id' not in data:  # 改为form里对应的xx_id
        return JsonResponse.fail(msg='需要传入staff_id')
    isOk = db.modify(sql='update staff set staff_name=%s,department=%s,salary=%s,phone_number=%s where staff_id=%s',  # 改为
                     args=[data['staff_name'], data['department'], data['salary'], data['phone_number'], data['staff_id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='修改失败')


@app.route("/delete_staff", methods=["DELETE"])  # 删除（单个）
def delete_staff():
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'staff_id' not in request.args:
        return JsonResponse.fail(msg='需要传入staff_id')
    isOk = db.modify(sql='delete from staff where staff_id=%s', args=[request.args['staff_id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')


# goods表
@app.route("/all_goods", methods=["GET"])  # 查询（全部）
def all_goods():
    result = db.get_list(sql='select * from goods')
    return JsonResponse.success(msg='查询成功', data=result)


@app.route("/add_goods", methods=["POST"])  # 添加（单个）
def add_goods():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into goods(goods_id,goods_name,goods_num) values(%s,%s,%s)',
                     args=[data['goods_id'], data['goods_name'], data['goods_num']])
    # python三元表达式
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')


@app.route("/update_goods", methods=["PUT"])  # 修改（单个）
def update_goods():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'goods_id' not in data:  # 改为form里对应的xx_id
        return JsonResponse.fail(msg='需要传入goods_id')
    isOk = db.modify(sql='update goods set goods_name=%s,goods_num=%s where goods_id=%s',  # 改为
                     args=[data['goods_name'], data['goods_num'], data['goods_id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='商品编号不可修改')


@app.route("/delete_goods", methods=["DELETE"])  # 删除（单个）
def delete_goods():
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'goods_id' not in request.args:
        return JsonResponse.fail(msg='需要传入goods_id')
    isOk = db.modify(sql='delete from goods where goods_id=%s', args=[request.args['goods_id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')

# purchase表
@app.route("/all_purchase", methods=["GET"])  # 查询（全部）
def all_purchase():
    result = db.get_list(sql='select * from purchase')
    return JsonResponse.success(msg='查询成功', data=result)


@app.route("/add_purchase", methods=["POST"])  # 添加（单个）
def add_purchase():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into purchase(purchase_id,staff_id,goods_id,purchase_price,purchase_num,purchase_amount,purchase_date) values(%s,%s,%s,%s,%s,%s,%s)',
                     args=[data['purchase_id'], data['staff_id'], data['goods_id'], data['purchase_price'], data['purchase_num'], data['purchase_amount'], data['purchase_date']])
    # python三元表达式
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')


@app.route("/update_purchase", methods=["PUT"])  # 修改（单个）
def update_purchase():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'purchase_id' not in data:  # 改为form里对应的xx_id
        return JsonResponse.fail(msg='需要传入purchase_id')
    sale_date = datetime.strptime(data['sale_date'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
    isOk = db.modify(sql='update purchase set staff_id=%s, goods_id=%s, purchase_price=%s, purchase_num=%s, purchase_amount=%s, purchase_date=%s  where purchase_id=%s',  # 改为
                     args=[data['staff_id'], data['goods_id'], data['purchase_price'], data['purchase_num'], data['purchase_amount'], sale_date])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='商品编号不可修改')


@app.route("/delete_purchase", methods=["DELETE"])  # 删除（单个）
def delete_purchase():
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'purchase_id' not in request.args:
        return JsonResponse.fail(msg='需要传入purchase_id')
    isOk = db.modify(sql='delete from purchase where purchase_id=%s', args=[request.args['purchase_id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')

#sale表
@app.route("/all_sale", methods=["GET"])  # 查询（全部）
def all_sale():
    result = db.get_list(sql='select * from sale')
    return JsonResponse.success(msg='查询成功', data=result)

@app.route("/add_sale", methods=["POST"])  # 添加（单个）
def add_sale():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into sale(sale_id, client_id, goods_id, sale_price, sale_num, sale_amount, sale_date) values(%s,%s,%s,%s,%s,%s,%s)',
                     args=[data['sale_id'], data['client_id'], data['goods_id'], data['sale_price'], data['sale_num'], data['sale_amount'], data['sale_date']])
    # python三元表达式
    return JsonResponse.success(msg='销售表添加成功') if isOk else JsonResponse.fail(msg='销售表添加失败')

@app.route("/update_sale", methods=["PUT"])  # 修改（单个）
def update_sale():
    # request.data获取请求体数据
    # 前端在发送请求时，由于指定了Content-Type为application/json；故request.data获取到的就是json数据
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'sale_id' not in data:  # 改为form里对应的xx_id
        return JsonResponse.fail(msg='需要传入sale_id')
    sale_date = datetime.strptime(data['sale_date'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
    isOk = db.modify(sql='update sale set client_id=%s,goods_id=%s,sale_price=%s,sale_num=%s,sale_amount=%s,sale_date=%s where sale_id=%s',  # 改为
                     args=[data['client_id'], data['goods_id'], data['sale_price'], data['sale_num'], data['sale_amount'], sale_date, data['sale_id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='修改失败')


@app.route("/delete_sale", methods=["DELETE"])  # 删除（单个）
def delete_sale():
    # request.args获取请求链接中 ? 后面的所有参数；以字典的方式存储
    if 'sale_id' not in request.args:
        return JsonResponse.fail(msg='需要传入sale_id')
    isOk = db.modify(sql='delete from sale where sale_id=%s', args=[request.args['sale_id']])
    return JsonResponse.success(msg='销售表删除成功') if isOk else JsonResponse.fail(msg='销售表删除失败')

# 运行flask：默认是5000端口，开启debug模式
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=666, debug=True)

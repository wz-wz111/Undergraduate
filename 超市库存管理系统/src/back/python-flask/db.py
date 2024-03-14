# # 数据库操作类

import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "sysu",
    "db": "supermarket",
    "charset": "utf8mb4"
}


class SQLManager(object):

    # 初始化实例方法
    def __init__(self):
        self.conn = None  # 连接对象，建立与MySQL数据库的连接
        self.cursor = None  # 游标对象，主要负责执行SQL语句
        self.connect()

    # 连接数据库
    def connect(self):
        # 建立连接
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            passwd=DB_CONFIG["passwd"],
            db=DB_CONFIG["db"],
            charset=DB_CONFIG["charset"]
        )
        # 获取游标对象；pymysql.cursors.DictCursor指定返回的结果类型为字典，默认是元组类型
        # 在连接没有关闭之前，游标对象可以反复使用
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询多条数据
    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)  # 执行SQL语句，返回受影响的行数
        return self.cursor.fetchall()  # 返回所有查询结果

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()  # 返回单条查询结果

    # 执行单条SQL语句
    def modify(self, sql, args=None):
        row = self.cursor.execute(sql, args)
        self.conn.commit()  # 对数据库的增、删、改操作需要提交事务，否则操作不生效
        return row > 0  # 若影响的行数>0，说明执行成功，返回True；否则返回False

    # 执行多条SQL语句
    def multi_modify(self, sql, args=None):
        rows = self.cursor.executemany(sql, args)
        self.conn.commit()
        return rows > 0

    # 关闭数据库cursor和连接
    def close(self):
        self.cursor.close()
        self.conn.close()

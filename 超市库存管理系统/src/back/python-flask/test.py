'''
Author：Jared
Date：2023年12月03日
'''

from db import *
db = SQLManager()
# result = db.get_list(sql="select * from public.user;")
result = db.get_list(sql="select * from sale")
print(result)


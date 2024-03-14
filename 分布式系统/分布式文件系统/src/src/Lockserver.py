# 锁服务器，用来实现对文件的上锁防止被同时写
import grpc
import time
import os

import LockServer_pb2 as LS_pb2  # 导入生成的 protobuf 文件
import LockServer_pb2_grpc as LS_pb2_grpc  # 导入生成的 protobuf 文件中的 gRPC 相关内容

from concurrent import futures  # 引入 futures 模块

from setup import *  # 导入自定义的配置文件

# lock_type = 1 -> 共享锁
# lock_type = 2 -> 排它锁
class LockServicer(LS_pb2_grpc.LockServerServicer):
    def __init__(self):
        # 初始化函数，设置服务器的 IP 地址、端口号以及文件路径等属性
        self.ip = lockServer_ip
        self.port = lockServer_port
        self.root_path = '../Server_data/Lock_server/'  # 服务器存储数据的根路径
        self.lockfile_name = 'Lock_info.txt'  # 存储锁信息的文件名
        self.lockfile_path = self.root_path + self.lockfile_name  # 锁文件的完整路径
        self.online()  # 在线状态提示

    def online(self):
        # 在线状态提示函数
        print("LockServer is online")

    def offline(self):
        # 离线状态提示函数
        print("LockServer is offline")

    # proto 服务
    def lockfile(self, request, context):
        try:
            self.addlock(request.file_path, request.filename, request.client_id, request.lock_type)  # 调用添加文件锁的方法
            success = 0  # 成功标志
        except Exception as e:
            print(e)
            success = 1  # 失败标志
        return LS_pb2.Lock_Reply(success=success)  # 返回上锁结果

    def unlockfile(self, request, context):
        try:
            self.unlock(request.file_path, request.filename, request.client_id)  # 调用解除文件锁的方法
            success = 0  # 成功标志
        except Exception as e:
            print(e)
            success = 1  # 失败标志
        return LS_pb2.Lock_Reply(success=success)  # 返回解锁结果

    def get_Lock_list(self):
        # 获取所有文件锁的信息
        f = open(self.lockfile_path, 'r', encoding='utf-8')
        lock_dic = {}  # 用字典存储文件锁的信息，以文件路径名作为索引
        for line in f.readlines():
            tmp = line.strip().split()
            if tmp != '':
                lock_dic[tmp[0]+tmp[1]] = {'filepath':tmp[0],'filename':tmp[1],'client_id': tmp[2], 'lock_type': tmp[3]}
        f.close()
        return lock_dic

    def addlock(self, filepath, filename, client_id, lock_type):
        # 添加文件锁
        lock_list = self.get_Lock_list()
        key = filepath + filename
        if key in lock_list and lock_list[key]['lock_type'] == '2':
            # 如果原来有锁，并且是排它锁，则不允许再次上锁
            raise Exception(f"Write_File({filepath}:{filename}) is locked ")

        if key in lock_list and lock_list[key]['lock_type'] == '1' and lock_type == 2:
            # 如果原来有读共享锁，并且现在要上排它锁，则不允许上锁
            raise Exception(f"Read_File({filepath}:{filename}) is locked ")

        # 新增锁信息到文件
        with open(self.lockfile_path, 'a', encoding='utf-8') as f:
            text = f"{filepath}\t{filename}\t{client_id}\t{lock_type}\n"
            f.write(text)
            if lock_type == 1:
            # print(f"New file lock ==>  filepath: {filepath}   filename: {filename}   client_id: {client_id}  lock_type: {lock_type}")
                print(f"Add read_lock to ({filepath}:{filename})   client_id: {client_id}  ")
            else:
                print(f"Add write_lock to ({filepath}:{filename})   client_id: {client_id}  ")
    def unlock(self, filepath, filename, client_id):
        # 解除文件锁
        server_dic = self.get_Lock_list()
        key = filepath + filename  # 锁的唯一标识
        if key in server_dic.keys() and server_dic[key]['client_id'] == str(client_id):
            del server_dic[key]  # 删除满足条件的键值对
            print(f"Unlock ({filepath}:{filename})   client_id: {client_id}  ")
            with open(self.lockfile_path, 'w', encoding='utf-8') as f:
                for id in sorted(server_dic):
                    text = str(server_dic[id]['filepath']) + '\t' + str(server_dic[id]['filename']) + '\t' + str(
                        server_dic[id]['client_id']) + '\n'  # 将删除后的字典重新写入文件
                    f.writelines(text)
        else:
            print("No matching lock found for the provided filepath, filename, and client_id.")


def run_server():
    servicer = LockServicer()  # 创建 LockServicer 实例
    if not os.path.exists(servicer.root_path):  # 如果数据的主文件夹不存在，则创建该文件夹和目标文件
        os.mkdir(servicer.root_path)
        open(servicer.lockfile_path, 'w', encoding='utf-8')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))  # 创建 gRPC 服务器
    LS_pb2_grpc.add_LockServerServicer_to_server(servicer, server)  # 将 LockServicer 添加到 gRPC 服务器
    server.add_insecure_port(f'[::]:{servicer.port}')  # 在指定端口启动服务器
    server.start()  # 启动服务器
    try:
        while True:
            time.sleep(60 * 60 * 24)  # 持续运行一天
    except KeyboardInterrupt:
        servicer.offline()  # 响应键盘中断，执行服务器下线操作
        server.stop(0)  # 停止服务器

if __name__=="__main__":
    run_server()  # 运行服务器

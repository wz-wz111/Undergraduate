import grpc
import time
import os

import DirectoryServer_pb2 as DS_pb2
import DirectoryServer_pb2_grpc as DS_pb2_grpc

from concurrent import futures
from setup import *

class DirectoryServer(DS_pb2_grpc.DirServerServicer):
    def __init__(self):
        self.ip = directoryServer_ip
        self.port = directoryServer_port
        self.root_path = '../Server_data/Directory_server/'  # 存储目录的根路径
        self.dirFile_name = 'Server_list.txt'  # 存储文件服务器信息的文件名
        self.path = os.path.join(self.root_path, self.dirFile_name)  # 存储文件的完整路径
        self.online()  # 启动时调用online方法

    # 重写DirServerServicer的函数
    def fileserver_online(self, request, context):
        try:
            self.addServer(request.Server_ID, request.ip, request.port, request.password)  # 调用addServer方法添加新的文件服务器
            success = 0  # 操作成功
        except Exception as e:
            print(e)
            success = 1  # 操作失败
        return DS_pb2.Dir_Reply(success=success)  # 返回结果给客户端

    def fileserver_offline(self, request, context):
        try:
            self.delServer(request.Server_ID)  # 调用delServer方法删除指定的文件服务器
            success = 0  # 操作成功
        except Exception as e:
            print(e)
            success = 1  # 操作失败
        return DS_pb2.Dir_Reply(success=success)  # 返回结果给客户端

    def getfileserver(self, request, context):
        server_dic = self.get_Server_list()
        server_list = []
        for id in sorted(server_dic):
            server_list.append(DS_pb2.FileServer_info(Server_ID=id, ip=server_dic[id]['ip'],
                                                     port=server_dic[id]['port'], password = server_dic[id]['password']))  # 将服务器信息添加到列表中
        return DS_pb2.FileServer_List(server_list=server_list)  # 返回包含服务器信息的列表给客户端

    # 自定义函数
    def online(self):
        print("DirServer is online")  # 输出在线状态信息

    def offline(self):
        print("DirServer is offline")  # 输出离线状态信息

    def get_Server_list(self):
        server_dic = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                tmp = line.strip().split()
                if tmp:
                    server_dic[int(tmp[0])] = {'ip': tmp[1], 'port': tmp[2], 'password': tmp[3]}
        return server_dic

    def addServer(self, id, ip, port, password):
        server_dic = self.get_Server_list()
        if id not in server_dic.keys():  # 如果id不存在于服务器列表中，则添加新的服务器信息
            with open(self.path, 'a', encoding='utf-8') as f:
                text = f"{id}\t{ip}\t{port}\t{password}\n"  # 格式化新的服务器信息为文本
                f.write(text)  # 写入文件
            print(f"ID: {id}   ip: {ip}   port: {port}    password:{password}")  # 输出新服务器登录信息

    def delServer(self, id):
        server_dic = self.get_Server_list()
        server_dic.pop(id)  # 删除指定id的服务器信息
        with open(self.path, 'w', encoding='utf-8') as f:
            for id in sorted(server_dic):
                text = f"{id}\t{server_dic[id]['ip']}\t{server_dic[id]['port']}\n"  # 将剩余的服务器信息格式化为文本
                f.write(text)  # 写入文件



def run_server():
    servicer = DirectoryServer()

    # 创建存储目录和文件
    if not os.path.exists(servicer.root_path):
        os.makedirs(servicer.root_path)
        open(servicer.path, 'w', encoding='utf-8').close()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    DS_pb2_grpc.add_DirServerServicer_to_server(servicer, server)
    server.add_insecure_port(f'[::]:{servicer.port}')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        servicer.offline()  # 调用offline方法
        server.stop(0)

if __name__ == "__main__":
    run_server()

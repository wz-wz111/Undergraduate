import os
import grpc
import FileServer_pb2 as FS_pb2, FileServer_pb2_grpc as FS_pb2_grpc
import DirectoryServer_pb2 as DS_pb2, DirectoryServer_pb2_grpc as DS_pb2_grpc
import LockServer_pb2 as LS_pb2, LockServer_pb2_grpc as LS_pb2_grpc
from setup import *

class FileClient:
    def __init__(self,id):
        self.id = id
        self.root_path = '../Client_data/Client_%s/'%(id)   # 客户端系统的根目录 为了简化文件系统，用户只有根目录不再创建子文件夹
        self.current_path = None # 客户端当前访问服务器的文件夹路径  初始为空
        self.CHUNK_SIZE = 1024 * 1024  # 1MB  传输文件的时候每次传1MB
        self.openfile_list=[]  # 客户端维护一个本地打开的文件队列


    def connect_dirserver(self):
        # 客户端首先连接到目录服务器  然后根据返回的文件服务器列表选择一个文件服务器
        dirchannel = grpc.insecure_channel(directoryServer_ip + ":" + directoryServer_port)
        self.dirstub = DS_pb2_grpc.DirServerStub(dirchannel)


    def connect_lockserver(self):
        # 客户接着需要连接到锁服务器
        lockchannel = grpc.insecure_channel(lockServer_ip + ":" + lockServer_port)
        self.lockstub = LS_pb2_grpc.LockServerStub(lockchannel)

    def choose_server(self):
        # 连接到文件锁服务器：
        print("Connecting to the file lock server...")
        self.connect_lockserver()

        # 连接目录服务器
        print("Connecting to the directory server...")
        self.connect_dirserver()

        # 从目录服务器中获取所有FS的信息
        while True:
            try:
                response = self.dirstub.getfileserver(DS_pb2.Dir_Empty(empty=0))
                break
            except:
                print("Directory server connection timed out!")
        print("Select one of the following servers:")
        server_dic = {}
        title = '{: <15}{: <15}{: <15}'.format('ServerID', 'IP', 'port')
        print(title)
        for server in response.server_list:
            server_dic[server.Server_ID] = {'ip': server.ip, 'port': server.port, 'password': server.password,
                                            'error_count': 0}  # 添加密码错误计数器
            info = '{: <15}{: <15}{: <15}'.format(str(server.Server_ID), server.ip, server.port)
            print(info)
        while True:
            pick = int(input("Input ServerID to choose: "))
            if pick not in server_dic.keys():
                print("Server does not exist, please select another server!")
                continue

            # 是否能登录该服务器
            error_count = 0  # 密码错误计数器
            while True:
                in_pwd = input(("Please input password:"))
                if in_pwd == server_dic[pick]['password']:
                    break
                else:
                    error_count += 1  # 密码错误计数器加一
                    print("Password Error")
                    if error_count == 3:  # 连续三次密码输入错误
                        print("Too many password errors! Please select another server.")
                        break

            if error_count == 3:  # 连续三次密码输入错误，重新选择服务器登录
                continue

            print("Connecting to file server...")
            try:
                # 记录连接的文件服务器地址
                self.FS_ip = server_dic[pick]['ip']
                self.FS_port = server_dic[pick]['port']
                channel = grpc.insecure_channel(self.FS_ip + ":" + self.FS_port)
                self.stub = FS_pb2_grpc.FileServerStub(channel)

                # 获取服务器的根目录地址，同时也可以检测服务器是否在线
                response = self.stub.pwd(FS_pb2.Empty(empty=0))
                self.current_path = response.pwd
                break
            except Exception as e:
                print("Server connection timed out, please select another server!")
                continue

    def save_chunks_to_file(self,chunks, target):
        with open(target, 'wb') as f:
            for chunk in chunks:
                f.write(chunk.buffer)


    def get_file_chunks(self,source,target):
        with open(source, 'rb') as f:
            while True:
                piece = f.read(self.CHUNK_SIZE)
                if len(piece) == 0:
                    return
                yield FS_pb2.Upload_Request(buffer=piece,target_path = target)  # 同时传文件和路径



    def upload(self, filename):
        # 用户上传文件， 上传完之后文件服务器需要同步到所有的副本上
        source = self.root_path + filename  # 上传文件的原地址
        target = self.current_path + filename  # 上传文件的目标地址 （服务器的地址）

        if self.lockfile(self.current_path, filename, 2) != 0:  # 对文件申请加锁
            print("The file is being written by someone else")
            return
        if not os.path.exists(source):
            print("files does not exist")
            return

        chunks_generator = self.get_file_chunks(source, target)
        response = self.stub.upload(chunks_generator)
        self.unlockfile(self.current_path, filename)# 解锁文件
        if response.success==0:
            print(f"Upload file({filename}) successfully!")
            return
        else:
            print("Upload failed!")
            return





    def download(self, filename):
        source = self.current_path + filename  # 远程服务器文件路径
        target = self.root_path + filename  # 下载到本地的路径
        source_filelist = self.list() #  获取远程服务器当前目录的文件，判断是否有目标文件

        if not filename in source_filelist: # 如果不存在就退出
            print("Target file does not exist")
            return

        if self.lockfile(self.current_path,filename,2) != 0: # 对文件申请加锁
            print("The file is being written by someone else")
            return

        response = self.stub.download(FS_pb2.Download_Request(download_path = source))
        if os.path.exists(target):
            # # 如果目标文件已经存在，就在名字后面加个 - copy n  n表示第几个副本
            tmp1 = os.listdir(self.root_path) # 获取当前所有文件名列表
            n=1
            for a in tmp1:  # 如果这个文件名字被当前文件包含，n就+1，  注意：文件名只有后缀才允许包含点
                if filename.split('.')[-2] in a and 'rename' in a:
                    n+=1
            ### 根据副本号n 生成新的目标文件名
            tmp2 = filename.split('.')
            tmp2[-2]+=" - rename%s"%(n)
            target = self.root_path + '.'.join(tmp2)
        self.save_chunks_to_file(response, target)
        print(f"Download file({filename}) successfully")

        self.unlockfile(self.current_path,filename) # 将文件解锁



    def delete(self,filename):
        ### 用户发消息删除文件服务器上的对应文件名
        target_filelist = self.list()  # 获取远程服务器当前目录的文件，判断是否有目标文件
        if not filename in target_filelist: # 如果不存在就退出
            print("Target file does not exist")
            return
        response = self.stub.delete(FS_pb2.Delete_Request(delete_path = self.current_path+filename))
        if response.success == 0:
            print(f"Delete file({filename}) successfully")
        else:
            print("Delete file failed")


    def write(self,filename):
        target_filelist = self.list()  # 获取远程服务器当前目录的文件，判断是否有目标文件
        if not filename in target_filelist:  # 如果不存在就退出
            print("Target file does not exist")
            return

        source = self.current_path + filename  # 远程服务器文件路径
        target = self.root_path + filename  # 下载到本地的路径
        source_filelist = self.list()  # 获取远程服务器当前目录的文件，判断是否有目标文件
        if not filename in source_filelist:  # 如果不存在就退出
            print("Target file does not exist")
            return

        if self.lockfile(self.current_path, filename, 2) != 0:  # 对文件申请加锁
            print("The file is being read or written by someone else")
            return

        response = self.stub.download(FS_pb2.Download_Request(download_path=source))

        self.save_chunks_to_file(response, target)
        print("Start writing")

        # 打开文件成功后将文件加入到已打开文件队列中去
        self.openfile_list.append((self.current_path,filename))


    def read(self,filename):
        target_filelist = self.list()  # 获取远程服务器当前目录的文件，判断是否有目标文件
        if not filename in target_filelist:  # 如果不存在就退出
            print("Target file does not exist")
            return

        source = self.current_path + filename  # 远程服务器文件路径
        target = self.root_path + filename  # 下载到本地的路径
        source_filelist = self.list()  # 获取远程服务器当前目录的文件，判断是否有目标文件
        if not filename in source_filelist:  # 如果不存在就退出
            print("Target file does not exist")
            return

        if self.lockfile(self.current_path, filename,1) != 0:  # 对文件申请加锁
            print("The file is being written by someone else")
            return

        response = self.stub.download(FS_pb2.Download_Request(download_path=source))

        # if os.path.exists(target):
        #     print("Warning: Local file with the same name is overwritten!")
        self.save_chunks_to_file(response, target)
        print("Start reading")

        # 打开文件成功后将文件加入到已打开文件队列中去
        self.openfile_list.append((self.current_path,filename))


    def close(self,filename):
        try:
            for i in range(len(self.openfile_list)):
                if filename == self.openfile_list[i][1]:
                    filepath,filename = self.openfile_list[i]
                    self.openfile_list.pop(i)  # 将文件从打开列表中取出
            # filepath,filename = self.openfile_list[id-1]  # id从1开始

            # self.unlockfile(filepath,filename)  # 对加锁文件解锁
            print("File closed successfully.")

            ## 将目标文件更新到远程服务器上
            source = self.root_path + filename  # 上传文件的原地址
            target = filepath + filename  # 上传文件的目标地址 （服务器的地址）

            # if self.lockfile(filepath, filename) != 0:  # 对文件申请加锁
            #     print("The file is being written by someone else")
            #     return

            if not os.path.exists(source):
                print("files does not exist")
                return
            chunks_generator = self.get_file_chunks(source, target)
            response = self.stub.upload(chunks_generator)

            self.unlockfile(filepath, filename)  # 解锁文件

            if response.success == 0:
                # print("File update successfully!")
                return
            else:
                print("File update failed!")
                return

        except Exception as e:
            print(e)
            print("File closed failed.")

    def list(self):
        ## 列出当前路径下的所有文件名 类似linux 的ls语句
        response = self.stub.list(FS_pb2.List_Request(cur_path = self.current_path))
        return response.list



    def lockfile(self, filepath,filename, lock_type):
        # 客户在下载文件或者打开文件的时候会对文件上锁，防止出现写写冲突
        response = self.lockstub.lockfile(LS_pb2.lockfileinfo(file_path=filepath, filename = filename, client_id = self.id, lock_type = lock_type))
        return response.success



    def unlockfile(self,filepath,filename):
        response = self.lockstub.unlockfile(LS_pb2.unlockfileinfo(file_path=filepath, filename = filename, client_id = self.id))
        return response.success




def run_client(id):
    # 建立客户端，并让用户自由选择一个在线的服务器进行连接
    client = FileClient(id)
    client.choose_server()

    if not os.path.exists(client.root_path):  # 创建数据的主文件夹
        os.mkdir(client.root_path)
    print("Successfully connect to FileServer %s" % (client.FS_ip + ":" + client.FS_port))
    root='$ '

    while True:
        print(root,end='')
        command = input().split()
        opera = command[0].lower()
        if opera=='ls':
            filelist = client.list()
            print(filelist)

        elif opera=='upload' or opera=='u':
            target_filename = command[1]  # 要上传的目标文件名字  名字要在当前的客户数据目录下
            client.upload(target_filename)

        elif opera=='download' or opera=='d':
            target_filename = command[1]  # 要下载的目标文件名字  名字要在当前的服务器数据目录下
            client.download(target_filename)

        elif opera == 'delete' or command[0]=='del':
            target_filename = command[1]
            client.delete(target_filename)

        elif opera == 'write':
            client.write(command[1])

        elif opera == 'read':
            client.read(command[1])

        elif opera == 'close':
            client.close(command[1])

        else:
            print("Please enter the correct command")



if __name__ == '__main__':
    # run_client(1)
    run_client(2)
# -*- coding: utf-8 -*-
import time
import zmq
import threading
import os
import shutil
import tarfile
import sys
sys.path.append("..")
import Config

class TarTcp:
    def __init__(self, ip, port, socket_type):
        self.ip = ip
        self.port = port
        self.socket_type = socket_type
        self.socket = self.init_socket()

    def init_socket(self):
        context = zmq.Context()
        _socket = context.socket(self.socket_type)
        if self.socket_type == zmq.REP:
            _socket.bind("tcp://" + self.ip + ":" + self.port)
        elif self.socket_type == zmq.REQ:
            _socket.connect("tcp://" + self.ip + ":" + self.port)
        print("<-----> Connecting to server! <----->")
        return _socket

    def recv_msg(self):
        msg = self.socket.recv()
        return msg

    def send_msg(self, msg):
        self.socket.send(msg)

    @staticmethod
    def unpack_tar(tar_path, save_path, flag_delete=False):
        """
        :param tar_path: 压缩包文件的相对路径
        :param save_path: 保存解压文件的文件夹相对路径
        :param flag_delete: 是否删除压缩包
        :return: file_path: 解压文件的绝对路径
        """
        tar = tarfile.open(tar_path)
        names = tar.getnames()
        file_path = os.path.abspath(tar_path.replace(Config.TAR_EXTENSION, '').replace('./tar/', save_path))
        if os.path.isdir(file_path):
            pass
        else:
            os.mkdir(file_path)
        for name in names:
            tar.extract(name, file_path)
        tar.close()

        if flag_delete:
            os.remove(tar_path)
        else:
            shutil.move(tar_path, "./trash/")
        return file_path

    def recv_package(self):
        while True:
            tar_name = self.recv_msg()  # recv --> 1st
            if "img" in tar_name:
                self.send_msg("Receive package name! " + time.strftime('%m-%d_%H:%M:%S',
                                                                       time.localtime(time.time())))  # send --> 1st:if

                tarfile = self.recv_msg()  # recv --> 2nd

                if len(tarfile) > 30:
                    tar_path = './tar/' + str(tar_name)
                    with open(tar_path, 'wb') as f:
                        f.write(tarfile)
                    # print "[Client: package]---> Success Receive package file:" + str(tar_name)
                    self.send_msg("Success Receive package file: " + str(tar_name))  # send --> 2nd:if
                else:
                    self.send_msg("[W: package #2]---> Receive package error! len(tarfile) > 30.")  # send --> 2nd:else
            else:
                self.send_msg("[W: package #1]---> Receive package error! No: tar_name")  # send --> 1st:else

    def recv_img(self, img_index):
        """
        接收图像
        :param img_index: 图像序号
        :return:  无
        """
        recv_tmp = self.recv_msg()  # recv --> 1st
        # print "[Debug]---> " + str(img_index)
        if "Waiting" in recv_tmp:
            print '[Client: image]---> ' + recv_tmp
            self.send_msg(str(img_index))  # send --> 1st:if
            tarfile = self.recv_msg()  # recv --> 2nd
            if len(tarfile) > 30:
                with open("./tar/" + "Original" + str(img_index) + Config.TAR_EXTENSION, 'wb') as f:
                    f.write(tarfile)
                print '[Client: image]---> Success Receive image file: ' + str(img_index) + Config.TAR_EXTENSION
                self.send_msg("Success Receive image file! ")  # send --> 2nd:if
            else:
                self.send_msg("[W: image #4]---> Receive image error! len(tarfile) < 30. ")  # send --> 2nd:else
        else:
            self.send_msg("[W: image #3]---> Receive image error! No: Waiting for request ...")  # send --> 1st:else

    def recv_all(self):
        """
        同时接收图片和切片
        """
        while True:
            tar_name = self.recv_msg()  # recv --> 1st
            if "img" in tar_name:
                print("[Client: package]---> Receive tar_name: " + tar_name)
                self.send_msg("Receive package name! " + time.strftime('%m-%d_%H:%M:%S', time.localtime(time.time())))  # send --> 1st:if
                tarfile = self.recv_msg()  # recv --> 2nd

                if len(tarfile) > 30:
                    tar_path = './tar/' + str(tar_name)
                    with open(tar_path, 'wb') as f:
                        f.write(tarfile)
                    print '[Client: package]---> Success Receive package file:' + str(tar_name)
                    self.send_msg("Success Receive package file: " + str(tar_name))  # send --> 2nd:if
                else:
                    self.send_msg("[W: package #2]---> Receive package error! len(tarfile) > 30.")  # send --> 2nd:else
            else:
                self.send_msg("[W: package #1]---> Receive package error! No: tar_name")  # send --> 1st:else


if __name__ == '__main__':
    inst_all = TarTcp('*', '25041', zmq.REP)  # 设置接收img的socket

    thd_recv_all = threading.Thread(target=inst_all.recv_all)
    thd_recv_all.setDaemon(True)
    thd_recv_all.start()

    # inst_tar = TarTcp('127.0.0.1', '25039', zmq.REP)
    # inst_img = TarTcp('127.0.0.1', '25040', zmq.REP)

    # thd_recv_package = threading.Thread(target=inst_tar.recv_package)
    # thd_recv_package.setDaemon(True)
    # thd_recv_package.start()

    # inst_tar2 = TarTcp('127.0.0.1', '25022', zmq.REP)
    # inst_img2 = TarTcp('127.0.0.1', '25023', zmq.REP)

    # thd_recv_package2 = threading.Thread(target=inst_tar2.recv_package)
    # thd_recv_package2.setDaemon(True)
    # thd_recv_package2.start()

    tmp = 0
    while True:
        tmp += 1
        # if tmp % 3 == 0:
        #     inst_img.recv_img(tmp)
        # else:
        #     inst_img.recv_img("None")

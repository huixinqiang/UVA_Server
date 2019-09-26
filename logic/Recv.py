import os
import threading
import logic.ZmqReceiver
import Config


class ReceiveData:
    def __init__(self, ip, port):
        """
                初始化压缩包index并连接网络接收压缩包
                :param ip: 发送端IP
                :param port: 发送端端口
                """
        self.index = 0
        for name in os.listdir('./tar'):
            subPath = os.path.join('./tar', name)
            if os.path.isfile(subPath):
                self.index += 1
        logic.ZmqReceiver.zmq_connect(ip, port)

    def recv_all(self):
        """
        同时接收图片和切片
        """
        while True:
            msg = logic.ZmqReceiver.recv_msg()  # recv
            msgLen = len(msg)
            if msgLen > 0:
                tar_path = './tar/img%d%s' % (self.index, Config.TAR_EXTENSION)
                try:
                    f = open(tar_path, 'wb')
                    f.write(msg)
                    f.close()
                    self.index += 1
                except OSError as err:
                    print(err)


if __name__ == '__main__':
    inst_all = ReceiveData(Config.SERVER_IP, Config.SERVER_PORT)  # 设置接收img的socket

    thd_recv_all = threading.Thread(target=inst_all.recv_all)
    thd_recv_all.setDaemon(True)
    thd_recv_all.start()
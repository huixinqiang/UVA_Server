# -*- coding: utf-8 -*-
import os
import threading
import socket

import Config
from logic.Recv import ReceiveData
from logic.Polling import PollingFile
from logic.PgSQL import PgSqlData


def start_zmq_thd():
    """
    开启zmq通信线程，接收数据
    :return: 无
    """
    inst_all = ReceiveData(Config.SERVER_IP, Config.SERVER_PORT)  # 设置接收img的socket

    thd_recv_all = threading.Thread(target=inst_all.recv_all)
    thd_recv_all.setDaemon(True)
    thd_recv_all.start()


def start_polling_thd():
    """
    开启文件轮询线程，解压新tar包
    :return: 无
    """
    db = PgSqlData(0, 0)
    pf = PollingFile(db)
    os.system('pause')
    db.db.close()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(e)
        return None

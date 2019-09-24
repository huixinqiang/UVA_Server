# coding=utf-8
import zmq

from logic.PgSQL import PgSqlData
from logic.util import *

# 根目录
ROOT_FOLDER = os.path.dirname(__file__)
os.environ['CUDA_VISIBLE_DEVICES'] = "0"

# SERVER_IP = get_host_ip()
SERVER_IP = '*'
SERVER_PORT = '25041'
SERVER_TYPE = zmq.REP

TAR_EXTENSION = ".tar.gz"

DB = PgSqlData(0, 0)

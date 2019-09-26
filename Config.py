# coding=utf-8
import os
from logic.PgSQL import PgSqlData

# 根目录
ROOT_FOLDER = os.path.dirname(__file__)
os.environ['CUDA_VISIBLE_DEVICES'] = "0"

# SERVER_IP = get_host_ip()
SERVER_IP = 'localhost'
SERVER_PORT = 25041

TAR_EXTENSION = ".tar.gz"

DB = PgSqlData(0, 0)

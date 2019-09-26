# coding=utf-8
import time
import json

from logic.util import *
import Config


class PollingFile:

    def __init__(self, db):
        self.data_path = ""

    @staticmethod
    def new_file_detector(path, sec):
        """
        新文件检测函数
        :param path: 文件路径
        :param sec: 扫描时间间隔
        :return: 新增文件
        """
        origin = set([_f[2] for _f in os.walk(path)][0])
        time.sleep(sec)
        final = set([_f[2] for _f in os.walk(path)][0])
        return final.difference(origin)

    @staticmethod
    def polling_file(db):
        """
        文件轮询函数并加入数据库db,应用于线程
        :param db: 数据库
        """
        new_tar_name = PollingFile.new_file_detector('./tar/', 1)
        for f in new_tar_name:
            new_tar_path = os.path.join('./tar/', f)
            if os.path.isfile(new_tar_path):
                data_path = Tar.unpack_tar(new_tar_path, './view/static/photos/')
                print ("The tar file \'" + f + "\' has been unpack.")

                db.add_db(data_path)
                load_dict = PollingFile.make_json(data_path, f)
                return load_dict

            else:
                print ("There is no file: " + str(new_tar_name))
                return None

    @staticmethod
    def find_newest_file(db):
        """
        查找最新的压缩包，解压并返回其json
        :param db: 数据库实例
        :return: dict格式的json
        """
        tar_path = os.path.join(Config.ROOT_FOLDER, "./tar/")
        max_id = PollingFile.get_max_img_id(tar_path)
        if max_id != 0:
            newest_tar_path = os.path.join(tar_path, "img" + str(max_id) + Config.TAR_EXTENSION)
            data_path = TarTcp.unpack_tar(newest_tar_path, './view/static/photos/')
            print ("The tar file \'" + data_path + "\' has been unpack.")

            db.add_db(data_path)
            tar_name = "img" + str(max_id) + Config.TAR_EXTENSION
            load_dict = PollingFile.make_json(data_path, tar_name)
            return load_dict
        else:
            return {}

    @staticmethod
    def get_max_img_id(folder):
        """
        找到最大id的压缩包
        :param folder:
        :return:
        """
        names = os.listdir(folder)
        ids = []
        for name in names:
            name = name.replace("img", "").replace(Config.TAR_EXTENSION, "")
            try:
                id = int(name)
                ids.append(id)
            except:
                pass
        if len(ids) == 0:
            max_id = 0
        else:
            max_id = max(ids)
        return max_id

    @staticmethod
    def make_json(data_path, f_name):
        """
        读取json文件并通过flask发送
        :param data_path: json文件路径
        :param f_name: 压缩包名
        :return: flask发送json
        """
        json_name = f_name.replace(Config.TAR_EXTENSION, ".json")
        json_path = os.path.join(data_path, json_name)
        with open(json_path, 'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict


if __name__ == '__main__':
    db = PgSqlData(0, 0)
    pf = PollingFile(db)
    os.system('pause')
    db.db.close()

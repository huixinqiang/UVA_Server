# -*- coding: utf-8 -*-
import os
import shutil
import tarfile
import sys
import Config

sys.path.append("..")


class Tar:
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

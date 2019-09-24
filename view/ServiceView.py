# coding=utf-8
import sys
import flask
import json
sys.path.insert(0, "..")

from view import app
from logic.util import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    开启接收线程
    :return: 状态
    """
    start_zmq_thd()  # 开启通信线程
    print ("<-----> Start Web Server! <----->")
    return "OK"


@app.route('/take_photo.json', methods=['GET', 'POST'])
def take_photo_json():
    """
    查找最新的图像和切片
    :return: 无
    """
    load_dict = PollingFile.find_newest_file(Config.DB)
    return flask.jsonify(load_dict)


@app.route('/retrieve_photo_by_id/<string:id>', methods=['GET', 'POST'])
@app.route('/retrieve_photo_by_id/<string:id>.json', methods=['GET', 'POST'])
def retrieve_photo_by_id(id):
    """
    :return:
    """
    json_path = os.path.join(
        Config.ROOT_FOLDER,
        "view/static/photos",
        "%s/%s.json" % (id, id)
    )
    if not os.path.exists(json_path):
        return flask.jsonify({})

    with open(json_path, "r") as fr:
        in_data = json.load(fr)
    return flask.jsonify(in_data)




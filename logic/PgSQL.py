# coding=utf-8

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (Session, interfaces, object_session, relationship, sessionmaker,)
import datetime
import json
import os


Base = declarative_base()


class TaskRecord(Base):
    """
    Task表
    TaskID: 任务ID，自增主键、外键
    User: User name
    TaskTime: 时间戳
    TaskLat: 纬度
    TaskLng: 经度
    TaskDescription:任务内容的备注信息
    """
    __tablename__ = 'Task'
    TaskID = Column(Integer, primary_key=True, autoincrement=True)
    User = Column(Unicode(255), default=u'Admin')
    TaskTime = Column(DateTime, nullable=False)
    TaskLat = Column(Float, default=40.0)
    TaskLng = Column(Float, default=116.0)
    TaskDescription = Column(Unicode(255))

    @classmethod
    def query_by_time(cls, db, q_time):
        """
        通过用时间查找数据库
        :param db:      数据库session
        :param q_time:    输入的名字
        :return:        record表中对应时间time的记录
        """
        return db.query(cls).filter(cls.TaskTime == q_time).first()

    @classmethod
    def query_by_id(cls, db, q_id):
        """
        通过用户的id查找数据库
        :param db: 数据库session
        :param q_id: 用户id
        :return: 表中对应id的记录
        """
        return db.query(cls).filter(cls.TaskID == q_id).first()

    @classmethod
    def query_by_id_interval(cls, db, q_id_start, q_id_end):
        """
        通过id区间查找数据库
        :param db:      数据库session
        :param q_id_start:  起始id
        :param q_id_end:    结束id
        :return:        表中对应id区间的记录
        """
        q1 = db.query(cls).filter(q_id_start <= cls.TaskID)
        q2 = q1.filter(cls.TaskID <= q_id_end)
        return q2.all()

    @classmethod
    def query_by_time_interval(cls, db, q_time_start, q_time_end):
        """
        通过时间段查找数据库
        :param db:      数据库session
        :param q_time_start:  起始time
        :param q_time_end:    结束time
        :return:        表中对应时间段的记录
        """
        q1 = db.query(cls).filter(q_time_start <= cls.TaskTime)
        q2 = q1.filter(cls.TaskTime <= q_time_end)
        return q2.all()

    @classmethod
    def get_ID(cls, db):
        return db.query(cls).order_by(cls.TaskID)[-1].TaskID


class FrameRecord(Base):
    """
    Frame表
    FrameID: 帧ID
    TaskID: 任务ID，与表Task对应
    UAVID: 飞机ID
    FrameTime: 帧时间戳
    FramePath: 帧保存路径
    FrameLat: 帧纬度
    FrameLng: 帧经度
    """
    __tablename__ = 'Frame'
    FrameID = Column(Integer, primary_key=True, autoincrement=True)
    TaskID = Column(Integer, ForeignKey('Task.TaskID'))
    UAVID = Column(Integer, default=0)
    FrameTime = Column(DateTime, nullable=false)
    FramePath = Column(Unicode(255))
    FrameLat = Column(Float)
    FrameLng = Column(Float)

    @classmethod
    def query_by_task_id(cls, db, q_id):
        """
        通过任务ID查找帧
        :param db:      数据库session
        :param q_id:  任务ID
        :return:        表中对应id的记录
        """
        return db.query(cls).filter(cls.TaskID == q_id).first()

    @classmethod
    def query_by_frame_id(cls, db, q_id):
        """
        通过帧ID查找帧
        :param db:     数据库session
        :param q_id:   任务id
        :return:   表中对应id的记录
        """
        return db.query(cls).filter(cls.FrameID == q_id).first()

    @classmethod
    def query_by_time(cls, db, q_time):
        """
        通过用时间查找帧
        :param db:      数据库session
        :param FrameTime:    帧时间
        :return:        record表中对应时间time的记录
        """
        return db.query(cls).filter(cls.FrameTime == q_time).first()

    @classmethod
    def query_by_time_interval(cls, db, q_time_start, q_time_end):
        """
        通过时间段查找数据库帧
        :param db:      数据库session
        :param q_time_start:  起始time
        :param q_time_end:    结束time
        :return:        表中对应时间段的记录
        """
        q1 = db.query(cls).filter(q_time_start <= cls.FrameTime)
        q2 = q1.filter(cls.FrameTime <= q_time_end)
        return q2.all()

    @classmethod
    def get_ID(cls, db):
        return db.query(cls).order_by(cls.FrameID)[-1].FrameID


class ClipRecord(Base):
    """
    Clip表
    ClipID: 切片ID
    FrameID: 帧ID,与表Frame对应
    TargetID: 目标ID
    ClipPath: 切片保存路径
    ClipLat: 切片纬度
    ClipLng: 切片经度
    ClipName: 帧目标名称（汽车、军车等等）
    """
    __tablename__ = 'Clip'
    ClipID = Column(Integer, primary_key=True, autoincrement=True)
    FrameID = Column(Integer, ForeignKey('Frame.FrameID'))
    ClipPath = Column(Unicode(255), nullable=false)
    ClipLat = Column(Float)
    ClipLng = Column(Float)
    ClipName = Column(Unicode(255), nullable=false)

    @classmethod
    def query_by_FrameID(cls, db, q_id):
        """
        通过帧ID查找切片
        :param db:      数据库session
        :param q_id:  帧ID
        :return:        表中对应id的记录
        """
        return db.query(cls).filter(cls.FrameID == q_id).all()

    @classmethod
    def get_ID(cls, db):
        return db.query(cls).order_by(cls.ClipID)[-1].ClipID


class PgSqlData:
    def __init__(self, task_lat, task_lng, user='uav_user', password='366432', host='127.0.0.1:5432', db_name='uav_data'):
        self.user = user
        self.password = password
        self.host = host
        self.database = db_name
        self.db = self.get_db()

        self.task = TaskRecord(TaskTime=datetime.datetime.now(), TaskLat=task_lat, TaskLng=task_lng)
        self.frame = null
        self.clip = null

        self.db.add(self.task)
        self.TaskID = self.task.get_ID(self.db)

        self.db.commit()

    def get_db(self):
        """
        初始化数据库，建立于数据库关联的session
        :param user: 数据库用户名
        :param host: ip和端口号
        :param database: 数据库名称
        :return: 返回Session对象
        """
        db_str = str('postgresql+psycopg2://{0}:{1}@{2}/{3}'.format(self.user, self.password, self.host, self.database))
        engine = create_engine(db_str, echo=True)
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        db = DBSession()
        return db

    def add_db(self, data_path):
        """
        为数据库增加新数据
        :param data_path: 数据文件夹路径
        :return:
        """
        if data_path.find('Original') != -1:
            # 只有原图数据
            frame_id = data_path[data_path.find('Original')+8:-1]
            json_path = os.path.join(data_path, "img" + frame_id + ".json")
            with open(json_path, 'r') as f:
                json_data = json.loads(f.read())
                query_res = FrameRecord.query_by_frame_id(self.db, q_id=frame_id)
                if query_res is None:
                    self.frame = FrameRecord(TaskID=self.TaskID , UAVID=0,
                                             FrameID=frame_id,
                                             FrameTime=datetime.datetime.strptime(json_data['img_time'], "%Y-%m-%d %H:%M:%S"),
                                             FramePath=Unicode(data_path, "utf-8"),
                                             FrameLng=json_data['FrameLng'],
                                             FrameLat=json_data['FrameLat']
                                             )
                    self.db.add(self.frame)
                else:
                    query_res.FramePath = data_path
                    self.db.add(query_res)
                f.close()
        else:
            # 切片与json数据
            frame_id = data_path[data_path.find('img') + 3:]
            json_path = os.path.join(data_path, "img" + frame_id + ".json")
            with open(json_path, 'r') as f:
                json_data = json.loads(f.read())
                self.frame = FrameRecord(TaskID=self.TaskID, UAVID=0,
                                         FrameID=frame_id,
                                         FrameTime=datetime.datetime.strptime(json_data['img_time'],
                                                                              "%Y-%m-%d %H:%M:%S"),
                                         FramePath=data_path,
                                         FrameLng=float(json_data['FrameLng']),
                                         FrameLat=float(json_data['FrameLat']))
                self.db.add(self.frame)
                clip_data = json_data['list']
                for l in clip_data:
                    clip = ClipRecord(FrameID=self.frame.FrameID, ClipPath=clip_data[l]['clip_path'],
                                      ClipLat=clip_data[l]['ClipLat'], ClipLng=clip_data[l]['ClipLng'],
                                      ClipName=clip_data[l]['name'])
                    self.db.add(clip)
                f.close()
        self.db.commit()


if __name__ == '__main__':
    db = PgSqlData(0, 0)
    db.add_db("D:\\Desktop\\img7\\")
    db.add_db("D:\\Desktop\\Original7\\")
    db.db.close()


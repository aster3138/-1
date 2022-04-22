from peewee import *
from . import db


class Proxy(Model):
    ip = CharField()  # ip
    port = IntegerField()  # 端口
    username = CharField()  # 账号
    password = CharField()  # 密码
    task_id = IntegerField()  # 任务id
    state = SmallIntegerField()  # 状态

    class Meta:
        database = db

    def to_dict(self) -> dict:
        return {'id': self.id, 'ip': self.ip, 'port': self.port, 'username': self.username, 'password': self.password,
                'task_id': self.task_id, 'state': self.state}

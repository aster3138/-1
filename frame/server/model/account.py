from peewee import *
from . import db

NOT_LOADED = 0
LOADED = 1


class Account(Model):
    username = CharField(default='')  # 账号
    password = CharField(default='')  # 密码
    name = CharField(default='')  # 名字
    level = SmallIntegerField(default=1)  # 等级
    proxy_id = IntegerField(default=0)  # 对应代理id
    task_id = IntegerField()  # 任务id
    is_load = SmallIntegerField(default=NOT_LOADED)  # 是否加载
    state = SmallIntegerField(default=0)  # 状态

    class Meta:
        database = db

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password, 'name': self.name,
                'level': self.level, 'proxy_id': self.proxy_id, 'task_id': self.task_id, 'is_load': self.is_load,
                'state': self.state}

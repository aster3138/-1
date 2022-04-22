from peewee import *
from . import db


class Task(Model):
    name = CharField()  # 名称
    script = CharField()  # 脚本名称
    interval = BigIntegerField()  # 启动间隔

    class Meta:
        database = db

    def to_dict(self) -> dict:
        return {'id': self.id, 'name': self.name, 'script': self.script, 'interval': self.interval}

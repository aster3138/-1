from peewee import *
from . import db
import random
import string


class User(Model):       # 创建继承  Model 的用户类
    username = CharField()  # 账号
    password = CharField()  # 密码
    salt = CharField()
    state = SmallIntegerField()

    class Meta:
        database = db

    def to_dict(self) -> dict:
        return {'id': self.id, 'username': self.username, 'state': self.state}

    def generator_salt(self, size=4):
        self.salt = ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

from peewee import DoesNotExist
from model.user import User
import hashlib
import jwt  # JWT 全称（Json WEB Token）是一种采用Json方式安装传输信息的方式。

KEY = "dsafklskfjlskdfjsiodfjosdfjslkfslkfsldfjs"


class UserException(BaseException):  # 创建继承 BaseException 的类
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def login_user(username: str, password: str) -> str:  # 用户登录
    try:
        user = User.get(username=username)
        password = hashlib.md5((user.salt + password).encode(encoding='UTF-8')).hexdigest()
        if user.password != password:
            raise UserException('账号或密码错误')
        return jwt.encode({"id": user.id}, KEY, algorithm="HS256")  # # 加密生成字符串， algorithm 为加密算法
    except DoesNotExist:
        raise UserException('账号或密码错误')


def create_user(username: str, password: str):
    count = User.select().count()

    if count >= 1:
        raise UserException('已存在账号禁止创建')

    user = User(username=username, state=0)
    user.generator_salt(size=4)
    password = hashlib.md5((user.salt + password).encode(encoding='UTF-8')).hexdigest()
    user.password = password
    user.save()


def decode_jwt(token):
    if token is None:
        raise UserException('未授权')

    try:
        return jwt.decode(token, KEY, algorithms=["HS256"])   # # 解密，校验签名
    except BaseException as err:
        raise err

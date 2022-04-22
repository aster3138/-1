from loguru import logger
from .client import Client
from model import Account, Proxy


class GameClient(Client):
    def __init__(self, a: Account, p: Proxy):
        Client.__init__(self, a, p)

    def to_dict(self):
        """后面在上面添加当前账号的其他信息"""
        d = Client.to_dict(self)
        return d
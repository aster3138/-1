import threading
from model import *
from service.controller.sub_controller import *


class TaskException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TaskController:
    def __init__(self, task: Task):
        self.__rlock = threading.RLock()
        self.__task = task
        self.__proxy_controller = ProxyController(self.__task.id)
        self.__client_controller = ClientController(self.__task.id)

    def get_id(self):
        return self.__task.id

    def get_task(self):
        return self.__task

    def load_account(self, count):
        """
        从数据库中加载账号
        加载账号同时需要ProxyController，所以不能在ClientController中实现
        """
        try:
            self.__rlock.acquire()
            cc = self.get_client_controller()
            # 此处为了方便写一条一条加载，后期有时间可以在修改
            while count > 0:
                a = Account.get(Account.is_load == NOT_LOADED)
                p = self.__proxy_controller.get_proxy(a.proxy_id)
                a.proxy_id = p.id  # 防止代理发生变更
                a.is_load = LOADED  # 将当前账号修改为已加载
                a.save()  # 同步修改去数据库
                count -= 1
                cc.add_client(a, p)
        except DoesNotExist:
            raise TaskException("无可用账号或账号数量不足")
        finally:
            self.__rlock.release()

    def delete_controller(self):
        try:
            self.__rlock.acquire()
            self.__client_controller.delete_controller()
            self.__proxy_controller.delete_controller()
            # 任务从数据库中删除
            self.__task.delete_instance()
        finally:
            self.__rlock.release()

    def get_proxy_controller(self):
        return self.__proxy_controller

    def get_client_controller(self):
        return self.__client_controller

    def update_task(self, **kwargs):
        self.__task.name = kwargs['name']
        self.__task.script = kwargs['script']
        self.__task.interval = kwargs['interval']
        self.__task.save()

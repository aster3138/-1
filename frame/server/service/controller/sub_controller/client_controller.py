import random
import string
import threading
from service.controller.sub_controller.client import *
from model import *


class ClientException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ClientController:
    def __init__(self, task_id: int):
        self.__rlock = threading.RLock()
        self.__task_id = task_id
        self.__list: [Client] = []

    def add_client(self, a: Account, p: Proxy):
        try:
            self.__rlock.acquire()
            self.__list.append(GameClient(a, p))  # 添加客户端
        finally:
            self.__rlock.release()

    def delete_controller(self):
        try:
            self.__rlock.acquire()
            # 关闭内存账号
            ids = self.__memory_ids()
            self.__close_by_ids(*ids)
            # 删除数据库
            Account.delete().where(Account.task_id == self.__task_id).execute()
        finally:
            self.__rlock.release()

    def generate_account(self, count):
        account_list = []
        while count > 0:
            count -= 1
            username = ''.join(random.choice(string.ascii_uppercase) for _ in range(4)) + '@xxx.com'
            password = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
            account_list.append(
                {'username': username, 'password': password, 'task_id': self.__task_id, 'is_load': NOT_LOADED})

        Account.insert_many(account_list).execute()

    def pagination(self, page: int, page_size: int, is_load: bool) -> (int, [dict]):
        try:
            self.__rlock.acquire()
            if is_load:
                return self.__memory_pagination(page, page_size)
            else:
                return self.__db_pagination(page, page_size)
        finally:
            self.__rlock.release()

    def batch_operate(self, task_info: Task, event: str, *ids: int):
        try:
            self.__rlock.acquire()
            if event == 'start':
                self.__start_by_ids(task_info.script, *ids)
            elif event == 'stop':
                self.__stop_by_ids(*ids)
            elif event == 'close':
                self.__close_by_ids(*ids)
            elif event == 'delete':
                self.__delete_by_ids(*ids)
            else:
                raise ClientException(f'未知操作事件:{event}')
        finally:
            self.__rlock.release()

    def __start_by_ids(self, script_name, *ids: int):
        try:
            self.__rlock.acquire()
            for account_id in ids:
                index = self.__get_index_by_id(account_id)
                if index is not None:
                    self.__list[index].start(script_name)
        finally:
            self.__rlock.release()

    def __stop_by_ids(self, *ids: int):
        try:
            self.__rlock.acquire()
            for account_id in ids:
                index = self.__get_index_by_id(account_id)
                if index is not None:
                    self.__list[index].stop()
        finally:
            self.__rlock.release()

    def __close_by_ids(self, *ids: int):
        for account_id in ids:
            index = self.__get_index_by_id(account_id)
            if index is not None:
                self.__list[index].close()
                acc = self.__list[index].get_account()
                acc.is_load = NOT_LOADED
                acc.save()
                del self.__list[index]

    def __delete_by_ids(self, *ids: int):
        # 删除内存
        self.__close_by_ids(*ids)
        # 删除数据库
        Account.delete().where(Account.id.in_(ids)).execute()

    def __memory_pagination(self, page: int, page_size: int) -> (int, [dict]):
        start_index = (page - 1) * page_size
        end_index = page * page_size
        total = len(self.__list)

        if start_index >= total:
            return total, []

        if end_index > total:
            end_index = total

        new_list: [dict] = []
        for item in self.__list[start_index:end_index]:
            d = item.to_dict()
            new_list.append(d)

        # new_list: [dict] = [item.to_dict() for item in self.__list[start_index:end_index]]
        return total, new_list

    def __db_pagination(self, page: int, page_size: int) -> (int, [dict]):
        total = Account.select().count()
        ls = Account.select().where(Account.task_id == self.__task_id).paginate(page, page_size)
        new_list: [dict] = [item.to_dict() for item in ls]
        return total, new_list

    def __memory_ids(self) -> [int]:
        """获取所有内存账号id"""
        ids: [int] = [item.get_id() for item in self.__list]
        return ids

    def __get_index_by_id(self, acc_id: int) -> int | None:
        index = 0
        while index < len(self.__list):
            if self.__list[index].get_id() == acc_id:
                return index
            index += 1
        return None

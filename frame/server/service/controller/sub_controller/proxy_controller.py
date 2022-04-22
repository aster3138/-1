import threading, copy
from model.proxy import Proxy


class ProxyException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ProxyController:
    def __init__(self, task_id: int):
        self.__index: int = 0  # 当前代理索引
        self.__rlock = threading.RLock()  # 访问安全控制
        self.__task_id: int = task_id  # 当前任务id
        self.__list: [Proxy] = []  # 当前代理

        self.__load_proxy_from_db()

    def get_proxy(self, proxy_id: int = 0) -> Proxy | None:
        """获取代理"""
        try:
            self.__rlock.acquire()
            length = len(self.__list)
            if length == 0:
                raise ProxyException("无可用代理")

            # 有旧代理，查找旧代理是否存在
            if proxy_id > 0:
                # 查找旧代理
                index = self.__get_index_by_id(proxy_id)
                if index != -1:
                    # 找到上次使用代理
                    return self.__list[self.__index]

            # 旧代理不存在，获取一个新代理
            self.__index = self.__index % length
            temp = self.__list[self.__index]
            self.__index += 1

            return temp
        finally:
            self.__rlock.release()

    def add_proxy(self, proxy_list: [dict]):
        """新添加代理"""
        try:
            self.__rlock.acquire()
            # 一条一条插入方便获取id
            for item in proxy_list:
                # 1.添加到数据库
                p = Proxy.create(**item)
                # 2.添加到内存中
                self.__list.append(p)
        finally:
            self.__rlock.release()

    def delete_proxy(self, *ids: [int]):
        """删除代理"""
        try:
            self.__rlock.acquire()
            # 1.先删除数据库
            Proxy.delete().where(Proxy.id.in_(ids))
            # 2.在删除内存
            for proxy_id in ids:
                index = self.__get_index_by_id(proxy_id)
                if index != -1:
                    del self.__list[index]
        finally:
            self.__rlock.release()

    def delete_controller(self):
        try:
            self.__rlock.acquire()
            # 1.从数据库删除
            Proxy.delete().where(Proxy.task_id == self.__task_id).execute()
            # 2.从内存中删除
            self.__list.clear()
        finally:
            self.__rlock.release()

    def pagination(self, page: int, page_size: int) -> (int, [dict]):
        try:
            self.__rlock.acquire()
            total = len(self.__list)
            start_index = (page - 1) * page_size
            end_index = page * page_size
            if start_index >= total:
                return total, []

            if end_index > total:
                end_index = total

            new_list: [dict] = [item.to_dict() for item in self.__list[start_index:end_index]]
            return total, new_list
        finally:
            self.__rlock.release()

    def __load_proxy_from_db(self):
        """从数据库加载代理"""
        try:
            self.__rlock.acquire()
            for proxy in Proxy.select():
                self.__list.append(proxy)
        finally:
            self.__rlock.release()

    def __get_index_by_id(self, proxy_id: int) -> int:
        index = 0
        while index < len(self.__list):
            if proxy_id == self.__list[index].id:
                return index
            index += 1
        return -1

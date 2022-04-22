import threading
import importlib
from typing import Any

from loguru import logger
from model import Account, Proxy


class ClientStopException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Client:
    def __init__(self, account: Account, proxy: Proxy):
        self.account = account
        self.proxy = proxy
        # 并发控制
        self.__rlock = threading.RLock()
        # 客户端状态
        self.__is_online = False
        self.__is_running = False
        self.__is_stop = False
        self.__script_name = ''
        self.__comment = ''

    def start_client(self, script_name: str):
        try:
            if self.__is_running:
                return
            self.__is_stop = False
            self.__is_running = True
            self.__script_name = script_name
            self.__comment = ''  # 清空之前日志
            # 启动日志
            self.info(f'start_client: {self.account.id}')
            # 启动脚本(脚本名不带后缀)
            module = importlib.import_module('static.script.' + self.__script_name)
            module.main(self)
        except ClientStopException as err:
            self.__comment = err.__str__()
            self.info(self.__comment)
        except BaseException as err:
            self.__comment = err.__str__()
            self.error(self.__comment)
        finally:
            self.__is_running = False

    def start(self, script_name: str):
        try:
            self.__rlock.acquire()
            if self.__is_running:
                # 已启动直接退出
                return
            threading.Thread(target=self.start_client, args=(script_name,)).start()
        finally:
            self.__rlock.release()

    def check_stop(self):
        if self.__is_stop:
            raise ClientStopException('主动停止')

    def stop(self):
        try:
            self.__rlock.acquire()
            self.info(f'stop_client: {self.account.id}')
            if self.is_running():
                self.__is_stop = True

        finally:
            self.__rlock.release()

    def close(self):
        # 未来可能需要等等当前账号完成关闭才退出
        self.__is_stop = True
        self.info(f'close_client: {self.account.id}')

    def to_dict(self) -> [dict]:
        d = self.account.to_dict()
        d['comment'] = self.__comment
        d['is_running'] = self.__is_running
        d['is_stop'] = self.__is_stop
        return d

    def get_account(self) -> Account:
        return self.account

    def get_id(self) -> int:
        return self.account.id

    def is_online(self):
        return self.__is_online

    def is_running(self):
        return self.__is_running

    def is_stop(self):
        return self.__is_stop

    def __log_prefix(self, __message: str, *args: Any, **kwargs: Any):
        return f'client {self.get_id()} ' + __message

    def debug(self, __message: str, *args: Any, **kwargs: Any):
        __message = self.__log_prefix(__message, *args, **kwargs)
        logger.debug(__message, *args, **kwargs)

    def info(self, __message: str, *args: Any, **kwargs: Any):
        __message = self.__log_prefix(__message, *args, **kwargs)
        logger.info(__message, *args, **kwargs)

    def warning(self, __message: str, *args: Any, **kwargs: Any):
        __message = self.__log_prefix(__message, *args, **kwargs)
        logger.warning(__message, *args, **kwargs)

    def error(self, __message: str, *args: Any, **kwargs: Any):
        __message = self.__log_prefix(__message, *args, **kwargs)
        logger.error(__message, *args, **kwargs)

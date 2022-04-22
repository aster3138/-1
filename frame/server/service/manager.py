import threading
from model import Task
from service.controller.task_controller import *


class Manager:
    def __init__(self):
        self.__rlock = threading.RLock()
        self.__list: [TaskController] = []
        self.__load_task_from_db()

    # 任务
    def create_task(self, task: Task):
        try:
            self.__rlock.acquire()
            # 1.保存数据库
            task.save()
            # 2.创建任务管理器
            tc = TaskController(task)
            # 3.添加列表
            self.__list.append(tc)
        finally:
            self.__rlock.release()

    def delete_task(self, task_id: int):
        try:
            self.__rlock.acquire()
            index = self.__get_index_by_task_id(task_id)
            if index is None:
                raise TaskException(f'任务id: {task_id}不存在')
            self.__list[index].delete_controller()
            del self.__list[index]
        finally:
            self.__rlock.release()

    def get_task_list(self) -> [dict]:
        try:
            self.__rlock.acquire()
            new_list: [dict] = [item.get_task().to_dict() for item in self.__list]
            return new_list
        finally:
            self.__rlock.release()

    def get_task_controller(self, task_id: int) -> TaskController:
        try:
            self.__rlock.acquire()
            index = self.__get_index_by_task_id(task_id)
            if index is None:
                raise TaskException(f'任务id: {task_id}不存在')

            return self.__list[index]
        finally:
            self.__rlock.release()

    def __load_task_from_db(self):
        """从数据库中加载任务"""
        try:
            self.__rlock.acquire()
            for item in Task.select():
                self.__list.append(TaskController(item))
        finally:
            self.__rlock.release()

    def __get_index_by_task_id(self, task_id: int) -> int | None:
        index = 0
        while index < len(self.__list):
            if self.__list[index].get_id() == task_id:
                return index
            index += 1
        return None


manager = Manager()

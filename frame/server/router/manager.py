import os

from flask import request
from service.manager import manager
from model import Task
from model.response.response import ok, fail, ok_with_list
from jsonschema import validate
from validate.manager import *
from . import manager_blue
from utils.tools import *


@manager_blue.route('/get-task-list', methods=['GET'])
def get_task_list():
    try:
        task_list = manager.get_task_list()
        return ok_with_list(msg='获取成功', list=task_list, total=len(task_list))
    except BaseException as err:
        return fail(err.__str__())


@manager_blue.route('/get-account-list', methods=['POST'])
def get_account_list():
    try:
        validate(request.json, validate_get_account)
        id = request.json['id']
        page = request.json['page']
        page_size = request.json['page_size']
        is_load = request.json['is_load']
        total, data_list = manager.get_task_controller(id).get_client_controller().pagination(page, page_size, is_load)
        return ok_with_list(msg='获取成功', list=data_list, total=total, page=page, page_size=page_size)
    except BaseException as err:
        return fail(err.__str__())


@manager_blue.route('/get-proxy-list', methods=['POST'])
def get_proxy_list():
    try:
        validate(request.json, validate_get_proxy)
        id = request.json['id']
        page = request.json['page']
        page_size = request.json['page_size']
        total, data_list = manager.get_task_controller(id).get_proxy_controller().pagination(page, page_size)
        return ok_with_list(msg='获取成功', list=data_list, total=total, page=page, page_size=page_size)
    except BaseException as err:
        return fail(err.__str__())


@manager_blue.route('/get-script-list', methods=['GET'])
def get_script_list():
    names = os.listdir(os.path.join('static', 'script'))
    list_data = []
    for item in names:
        if not item.endswith('.py'):
            # 过滤不是.py文件
            continue
        list_data.append({'label': item, 'value': item.replace('.py', '', -1)})
    return ok_with_list(msg='获取成功', list=list_data, total=len(list_data))


# 任务相关
@manager_blue.route('/create-task', methods=['POST'])
def create_task():
    try:
        validate(request.json, validate_create_task)
        manager.create_task(
            Task(name=request.json['name'], script=request.json['script'], interval=request.json['interval']))
        return ok('创建成功')
    except BaseException as err:
        return fail(err.__str__())


@manager_blue.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        manager.delete_task(task_id)
        return ok(msg='删除成功')
    except BaseException as err:
        return fail(msg=err.__str__())


@manager_blue.route('/update-task', methods=['PUT'])
def update_task():
    try:
        validate(request.json, validate_update_task)
        task_id = request.json['id']
        manager.get_task_controller(task_id).update_task(**request.json)
        return ok(msg='更新成功')
    except BaseException as err:
        return fail(msg=err.__str__())


# 账号相关
@manager_blue.route('/generate-account', methods=['POST'])
def generate_account():
    try:
        validate(request.json, validate_generate_account)
        task_id = request.json['id']
        count = request.json['count']
        manager.get_task_controller(task_id).get_client_controller().generate_account(count)
        return ok(msg='生成成功')
    except BaseException as err:
        return fail(msg=err.__str__())


@manager_blue.route('/load-account', methods=['POST'])
def load_account():
    try:
        validate(request.json, validate_load_account)
        task_id = request.json['id']
        count = request.json['count']
        manager.get_task_controller(task_id).load_account(count)
        return ok(msg='加载成功')
    except BaseException as err:
        return fail(msg=err.__str__())


# 客户端
@manager_blue.route('/batch-operate-client', methods=['POST'])
def batch_operate_client():
    try:
        validate(request.json, validate_batch_operate_client)
        id = request.json['id']
        ids = request.json['ids']
        event = request.json['event']
        tc = manager.get_task_controller(id)
        cc = tc.get_client_controller()
        cc.batch_operate(tc.get_task(), event, *ids)
        return ok(msg='操作成功')
    except BaseException as err:
        return fail(msg=err.__str__())


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 代理相关
@manager_blue.route('/upload-proxy', methods=['POST'])
def upload_proxy():
    try:
        file = request.files['file']
        if file is None:
            return fail('没有上传文件')
        if not allowed_file(file.filename):
            return fail('禁止上传的格式')

        # 将代理解析成map
        id = int(request.form.get('id'), 10)
        proxy_list = parse_upload_proxy(file.read(), id)
        manager.get_task_controller(id).get_proxy_controller().add_proxy(proxy_list)
        return ok(msg='上传成功')
    except BaseException as err:
        return fail(msg=err.__str__())


@manager_blue.route('/delete-proxy', methods=['DELETE'])
def delete_proxy():
    try:
        validate(request.json, validate_delete_proxy)
        id = request.json['id']
        ids = request.json['ids']
        manager.get_task_controller(id).get_proxy_controller().delete_proxy(*ids)
        return ok(msg='操作成功')
    except BaseException as err:
        return fail(msg=err.__str__())

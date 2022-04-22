from loguru import logger
from flask import request, make_response, g
from . import user_blue
from jsonschema import validate
from validate.user import validate_username_password
from model.response.response import ok, fail
from service.user import create_user, login_user


@user_blue.route('/login', methods=['POST'])
def login():
    try:
        validate(request.json, validate_username_password)
        username = request.json['username']
        password = request.json['password']
        jwt = login_user(username, password)
        res = make_response(ok(msg='登录成功'))
        res.headers['New-Token'] = jwt
        logger.info(f'path: {request.path} username: {username} jwt: {jwt}')
        return res
    except BaseException as err:
        logger.error(f'path: {request.path} error: {err.__str__()}')
        return fail(msg=err.__str__())


@user_blue.route('/logout', methods=['GET'])
def logout():
    logger.info(f'path: {request.path}')
    return ok(msg='登出成功')


@user_blue.route('/create', methods=['POST'])
def create():
    try:
        validate(request.json, validate_username_password)
        username = request.json['username']
        password = request.json['password']
        create_user(username, password)
    except BaseException as err:
        return fail(msg=err.__str__())

    return ok(msg='创建成功')


@user_blue.route('/user-info', methods=['GET'])
def user_info():
    return ok(msg='', data=g.user.to_dict())

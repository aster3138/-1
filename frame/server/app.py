import sys
from flask import Flask, request, make_response, g
import yaml
from model import *
from loguru import logger

# 以下是自定义模块
from router import user_blue, manager_blue
from model.response.response import *
from service.user import decode_jwt

app = Flask(__name__)

# 加载配置
configure_file: str = 'config.dev.yaml' if app.config.get('ENV') == 'development' else 'config.yaml'
app.config.update(**yaml.load(open(configure_file).read(), Loader=yaml.Loader))

# 初始化日志
logger.remove()  # 移除默认
loguru_dict: dict = app.config.get('loguru')  # 获取日志配置
logger.add("static/logs/log_{time}.log", level=loguru_dict.get('level'), rotation=loguru_dict.get('rotation'))  # 输出日志
logger.add(sys.stdout, level=loguru_dict.get('level'))  # 输出控制台


@app.before_request
def handle_before():
    # 跨域检测
    if request.method == 'OPTIONS':
        res = make_response('', 200)
        return res

    # 登录/登出请求放行
    white_list = ['/api/user/login', '/api/user/logout', '/api/user/create']
    if request.path in white_list:
        return None

    # 拦截非法请求
    token = request.headers.get('Token', None)
    try:
        id = decode_jwt(token)['id']
        # 将用户信息保存到全局对象上
        g.user: User = User.get(User.id == id)
        logger.debug(f"path: {request.path} user_id: {g.user.id}")
    except BaseException as err:
        logger.error(f"path: {request.path} error: {err.__str__()}")
        return result(UN_AUTH, err.__str__(), None)


@app.after_request
def handle_after(res):
    # 允许访问头
    res.headers['Access-Control-Expose-Headers'] = 'New-Token'
    # 允许跨域
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Token'
    res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return res


# 注意路由
app.register_blueprint(manager_blue)
app.register_blueprint(user_blue)

# 将所有账号修改为可用
Account.update({Account.is_load: NOT_LOADED}).where(Account.is_load == LOADED).execute()

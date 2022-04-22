from flask import Blueprint

user_blue = Blueprint('user', __name__, url_prefix='/api/user')
manager_blue = Blueprint('manager', __name__, url_prefix='/api/manager')

from . import manager, user

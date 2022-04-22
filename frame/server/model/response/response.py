SUCCESSFUL: int = 0  # 成功
ERROR: int = -1  # 遇到错误
UN_AUTH: int = -2  # 未授权


def result(code: int, msg: str, data: any):
    return {'code': code, 'msg': msg, 'data': data}


def ok(msg='', data=None):
    return result(SUCCESSFUL, msg, data)


def fail(msg='', data=None):
    return result(ERROR, msg, data)


def ok_with_list(msg='', list: [dict] = [], total: int = 0, page: int = 0, page_size: int = 0):
    return result(SUCCESSFUL, msg, {'list': list, 'total': total, 'page': page, 'page_size': page_size})

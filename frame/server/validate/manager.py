validate_create_task = {      # 验证创建任务
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'script': {'type': 'string'},
        'interval': {'type': 'number'},
    },
    'required': ['name', 'script', 'interval']
}

validate_update_task = {       # 验证更新任务
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'name': {'type': 'string'},
        'script': {'type': 'string'},
        'interval': {'type': 'number'},
    },
    'required': ['name', 'script', 'interval']
}

validate_get_proxy = {         # 验证获取代理
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'page': {'type': 'number'},
        'page_size': {'type': 'number'},
    },
    'required': ['id', 'page', 'page_size']
}

validate_get_account = {      # 验证获取帐户
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'page': {'type': 'number'},
        'page_size': {'type': 'number'},
        'is_load': {'type': 'number'},
    },
    'required': ['id', 'page', 'page_size', 'is_load']
}

validate_generate_account = {   # 验证生成帐户
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'count': {'type': 'number'},
    },
    'required': ['id', 'count']
}

validate_batch_operate_client = {   # 验证批处理操作客户端
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'ids': {'type': 'array'},
        'event': {'type': 'string'},
    },
    'required': ['id', 'ids', 'event']
}

validate_delete_proxy = {           # 验证删除代理
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'ids': {'type': 'array'},
    },
    'required': ['id', 'ids']
}

validate_load_account = {           # 验证加载帐户
    'type': 'object',
    'properties': {
        'id': {'type': 'number'},
        'count': {'type': 'number'},
    },
    'required': ['id', 'count']
}

from io import StringIO


class ParseProxyException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def parse_upload_proxy(data: bytes, id: int) -> [dict]:
    sio = StringIO(data.decode(encoding='UTF-8'))
    p_list: [dict] = []
    line_count = 0
    while True:
        line_count += 1
        line = sio.readline()
        if line == '':
            break

        # 替换\r\n
        line = line.replace('\r', '', -1)
        line = line.replace('\n', '', -1)
        if line == '':
            continue
        s_list = line.split('|', -1)
        # ip|port|username|password
        if (len(s_list) != 4) or not s_list[1].isalnum() or len(s_list[0]) == 0:
            # 长度不等于4 or 端口不是数字 or ip为空
            raise ParseProxyException(f'行号: {line_count},内容: {line}')
        p_list.append(
            {'ip': s_list[0], 'port': int(s_list[1], 10), 'username': s_list[2], 'password': s_list[3], 'task_id': id,
             'state': 0})

    return p_list

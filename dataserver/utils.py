import json
import os
import uuid


def tojson(res, msg='', data={}):
    return json.dumps({'res': res, 'msg': msg, 'data': data})


def get_uuid():
    if os.path.exists('.uuid'):
        with open('.uuid', 'r') as f:
            uid = f.read()
    else:
        uid = uuid.uuid1().hex
        with open('.uuid', 'w') as f:
            f.write(uid)

    return uid

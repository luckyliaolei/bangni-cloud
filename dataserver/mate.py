from flask import (
    Blueprint, request
)

from auth import login_required
from db import files, nodes
bp = Blueprint('mate', __name__)

@bp.route('/')
def hello_world():
    return '"Hello World!"'


@bp.route('/md5')
@login_required
def md5():
    filename = request.args.get('filename')
    files.insert({'filename': filename, 'chunks': [{'hash': '', 'nodes': ['']}]})
    return 'ok'


@bp.route('/report')
def report():
    nodes.update({'ip': request.remote_addr, 'chunks': [{'hash': 'sdfsfs', 'nodes': ['127.0.0.1']}]}, )
    return '"Hello World!"'
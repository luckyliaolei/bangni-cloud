from flask import (
    Blueprint, request, session
)

from auth import login_required
from db import files, nodes, users, chunks
from utils import tojson
from bson.objectid import ObjectId
bp = Blueprint('mate', __name__)

@bp.route('/')
def hello_world():
    return '"Hello World!"'


@bp.route('/mate/newfile')
@login_required
def mate():
    filename = request.args.get('filename')
    users.update_one({'_id': session['user_id']})
    r = files.insert_one({'filename': filename, 'hash': '', 'chunks': []})
    return tojson(True, '', r['_id'].binary.hex())


@bp.route('/mate/chunk')
@login_required
def mate():
    file_id = request.args.get('file_id')
    index = request.args.get('index')
    chunk_hash = request.args.get('chunk_hash')
    uuid = request.args.get('uuid')
    _id = ObjectId(file_id)
    files.update_one({'_id': _id}, {'$set': {'chunks.' + index + '.hash': chunk_hash}})
    chunks.insert_one({'hash': chunk_hash, 'node_uuid': uuid})
    return tojson(True, '')


@bp.route('/mate/success')
@login_required
def mate():
    file_id = request.args.get('file_id')
    file_hash = request.args.get('file_hash')
    _id = ObjectId(file_id)
    files.update_one({'_id': _id}, {'$set': {'hash': file_hash},
                                    '$currentDate': {'success_date': True}})
    return tojson(True, '')

@bp.route('/report')
def report():
    volume = request.args.get('volume')
    remain = request.args.get('filename')
    uuid = request.args.get('uuid')
    nodes.update_one({'uuid': uuid}, {'ip': request.remote_addr, 'volume': volume, 'remain': remain}, {'upsert': True})
    return tojson(True, '')


@bp.route('/nodes')
def nodes():
    r = nodes.find({}, {'ip': 1, '_id': 0})
    return tojson(True, '', r)


@bp.route('/list')
def list():
    _id = session['user_id']
    r = users.find_one({'_id': _id})
    return tojson(True, '', r['files'])

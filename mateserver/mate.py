from flask import (
    Blueprint, request, session
)

from auth import login_required
from db import files, nodes, users
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
    file_hash = request.args.get('file_hash')
    if files.find_one({
                              '_id': file_hash}):
        return tojson(1, 'success')

    elif users.find({
                           'files': {
                               '$all': [file_hash]}}):
        return tojson(2, 'file exist')

    else:
        files.insert_one({
            '_id': file_hash,
            'filename': filename,
            'chunks': []})  # {chunk_hash: '', nodes: []}
        users.update_one({
            '_id': ObjectId(session['user_id'])}, {
            '$push': {
                'files': file_hash}})
        return tojson(0, '')


@bp.route('/mate/chunk')
@login_required
def chunk():
    file_hash = request.args.get('file_hash')
    chunk_index = request.args.get('chunk_index')
    chunk_hash = request.args.get('chunk_hash')
    uuid = request.args.get('uuid')
    files.update_one({
                         '_id': file_hash}, {
                         '$set': {
                             'chunks.' + chunk_index: {
                                 'chunk_hash': chunk_hash}}})
    files.update_one({
                         '_id': file_hash}, {
                         '$push': {
                             'chunks.' + chunk_index + '.nodes': uuid}})

    # nodes.update_one({
    #                      'uuid': uuid}, {
    #                      '$push': {
    #                          'chunks': chunk_hash}})
    return tojson(True, '')


@bp.route('/mate/success')
def success():
    file_hash = request.args.get('file_hash')
    files.update_one({
                         '_id': file_hash}, {
                         '$currentDate': {
                             'success_date': True}})
    users.update_one({
                         '_id': ObjectId(session['user_id'])}, {
                         '$push': {
                             'files': file_hash}})
    return tojson(True, '')


@bp.route('/mate/file-mate')
def file_mate():
    file_hash = request.args.get('file_hash')
    r = files.aggregate(
        [{
             "$match": {
                 "_id": file_hash}}, {
             "$unwind": "$chunks"}, {
             "$unwind": "$chunks.nodes"},
         {
             "$lookup": {
                 "from": "nodes",
                 "localField": "chunks.nodes",
                 "foreignField": "uuid",
                 "as": "nodes"}},
         {
             "$project": {
                 "_id": 0,
                 "chunk_hash": "$chunks.chunk_hash",
                 "nodes": "$nodes.ip"}}])
    return tojson(True, '', list(r))


@bp.route('/mate/delete-file')
@login_required
def delfile():
    file_hash = request.args.get('file_hash')
    users.update_one({
            '_id': ObjectId(session['user_id'])}, {
            '$pullAll': {
                'files': [file_hash]}})
    return tojson(1, 'delete success')


@bp.route('/report')
def report():
    volume = request.args.get('volume')
    uuid = request.args.get('uuid')
    nodes.update_one({
                         'uuid': uuid}, {
                         '$set': {
                             'ip': request.remote_addr,
                             'volume': int(volume),
                             }}, upsert=True)
    return tojson(True, '')


@bp.route('/get-nodes')
def get_nodes():
    r = nodes.find({}, {
        'ip': 1,
        'uuid': 1,
        '_id': 0}).limit(10)
    return tojson(True, '', list(r))


@bp.route('/list')
def list_user_file():
    _id = ObjectId(session['user_id'])
    r = users.find_one({
                           '_id': _id})
    r = files.find({
                       '_id': {
                           '$in': r['files']}}, {
                       'filename': 1})
    return tojson(True, '', list(r))


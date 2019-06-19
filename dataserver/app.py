from flask import Flask, request
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
files = client['test']['files']
hosts = client['test']['hosts']
users = client['test']['users']
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '"Hello World!"'


@app.route('/md5')
def md5():
    filename = request.args.get('filename')
    files.insert({'filename': filename, 'chunks': [{'hash': 'sdfsfs', 'nodes': ['127.0.0.1']}]})
    return '"Hello World!"'


@app.route('/report')
def md5():
    request.
    col.insert({'ip': request.remote_addr, 'chunks': [{'hash': 'sdfsfs', 'nodes': ['127.0.0.1']}]}, )
    return '"Hello World!"'


@app.route('/user')
def md5():
    users.insert({'ip': request.remote_addr, 'chunks': [{'hash': 'sdfsfs', 'nodes': ['127.0.0.1']}]}, )
    return '"Hello World!"'


@app.route('/login')
def md5():
    users.insert({'ip': request.remote_addr, 'chunks': [{'hash': 'sdfsfs', 'nodes': ['127.0.0.1']}]}, )
    return '"Hello World!"'


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save('chunks/' + f.filename)
    return 'ok'


if __name__ == '__main__':
    app.run()

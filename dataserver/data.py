from flask import (
    request, Flask
)
import os
import requests
from utils import get_uuid

app = Flask(__name__, static_folder='chunks')
mate_server = 'http://124.16.70.103:5000'
uuid = get_uuid()
r = requests.get(mate_server + '/report', params={'uuid': uuid, 'volume': 2})
print(r.json()['msg'])


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save('chunks/' + f.filename)
    return 'ok'


@app.route('/download', methods=['POST'])
def download():
    filename = request.args.get('filename')
    return filename


@app.route('/download', methods=['POST'])
def delete():
    chunks = request.form['chunks']
    for chunk in chunks.split(','):
        os.remove('chunks/' + chunk)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
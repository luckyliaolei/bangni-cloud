import hashlib
import getopt
import os
import sys
import requests
import shutil
import threading
import queue
import progressbar
import time

mate_server = 'http://127.0.0.1:5000'
chunk_size = 8 * 2 ** 20  # 8 MB
files = None  # [{'_id': '', 'filename': ''}]


def usage():
    u = '''
    Name:
        %s - object storage client

    Synopsis:
        %s [-u] [-p]
    Description:
        Arguments are as following
            -u  username
            -p  password
    '''
    prog = os.path.basename(sys.argv[0])
    print(u % (prog, prog))
    sys.exit(0)


def list_file():
    global files
    r = s.get(mate_server + '/list')
    r = r.json()
    if r['res']:
        files = r['data']
        if not files:
            print('no file, please upload at first')
            return

        for i, file in enumerate(files):
            print(i, file['filename'])


def upload(filename):
    r = s.get(mate_server + '/get-nodes')
    nodes = r.json()['data']

    if not os.path.isfile(filename):
        print('No such file: ' + filename)
        return

    f = open(filename, 'rb')

    md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(chunk_size), b''):
        md5.update(chunk)

    file_hash = md5.hexdigest()
    r = s.get(mate_server + '/mate/newfile', params={
        'filename': filename,
        'file_hash': file_hash})
    r = r.json()
    if r['res'] is 1:
        return 'upload successful'

    q = queue.Queue(2)

    def upload_th(node):
        while True:
            chunk_dict = q.get()
            chunk_hash = hashlib.md5(chunk_dict['chunk']).hexdigest()
            chunk = chunk_dict['chunk']
            s.get(mate_server + '/mate/chunk',
                  params={
                      'chunk_hash': chunk_hash,
                      'file_hash': file_hash,
                      'chunk_index': chunk_dict['chunk_index'],
                      'uuid': node['uuid']})
            s.post('http://' + node['ip'] + ':5001/upload', files={
                'file': (chunk_hash, chunk)})
            q.task_done()

    for node in nodes:
        threading.Thread(target=upload_th, args=(node,)).start()

    chunk_index = 0
    f.seek(0)
    chunk_num = os.path.getsize(filename) // chunk_size
    p = progressbar.ProgressBar(chunk_num + 1)
    p.start()
    for tmp_chunk in iter(lambda: f.read(chunk_size), b''):
        md5.update(tmp_chunk)
        q.put({
                  'chunk_index': chunk_index,
                  'chunk': tmp_chunk})
        chunk_index += 1
        p.update(chunk_index)
    p.finish()
    q.join()
    s.get(mate_server + '/mate/success', params={
        'file_hash': file_hash})
    return 'upload successful'


def download(index):
    if not files:
        return 'please list the files at first!'

    file_hash = files[index]['_id']
    response = s.get(mate_server + '/mate/file-mate', params={
        'file_hash': file_hash})
    r_mate = response.json()

    ips_chunk = {}

    def download_th(node_ip):
        while True:
            chunk_hash = ips_chunk[node_ip].get()
            r_chunk = s.get('http://' + node_ip + ':5001/chunks/' + chunk_hash,  stream=True)
            # Throw an error for bad status codes
            r_chunk.raise_for_status()
            with open('tmp/' + chunk_hash, 'wb') as handle:
                for block in r_chunk.iter_content(1024):
                    handle.write(block)
            ips_chunk[node_ip].task_done()

    for chunk in r_mate['data']:
        new_nodes = set(chunk['nodes']) - set(ips_chunk.keys())
        if new_nodes:
            q = queue.Queue()
            ip = new_nodes.pop()
            q.put(chunk['chunk_hash'])
            ips_chunk[ip] = q
            threading.Thread(target=download_th, args=(ip,)).start()
        else:
            ips_chunk[chunk['nodes'][0]].put(chunk['chunk_hash'])

    for chunks_queue in ips_chunk.values():
        chunks_queue.join()

    with open('src/' + files[index]['filename'], 'wb') as wfd:
        for f in r_mate['data']:
            with open('tmp/' + f['chunk_hash'], 'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    return 'download successful'

def delete(index):
    r = s.get(mate_server + '/mate/delete-file', params={
        'file_hash': files[index]['_id']})
    return  r.json()['msg']

def login(name, passwd):
    s = requests.session()
    r = s.get(mate_server + '/auth/login', params={
        'name': name,
        'passwd': passwd})
    r = r.json()
    if r['res']:
        return s
    else:
        print(r['msg'])
        sys.exit(0)


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:p:', "help")
    except getopt.GetoptError as e:
        sys.exit(1)

    name = 'liao'
    passwd = 'll'

    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
        elif op == "-u":
            name = value
        elif op == "-p":
            passwd = value

    s = login(name, passwd)
    print('Log in successful, please input commend!')

    while True:
        line = input()
        cmd, *op = line.split(' ')
        if cmd == 'q':
            sys.exit(0)
        elif cmd == 'ls':
            list_file()
        elif cmd == 'lsl':
            for file_name in os.listdir():
                if os.path.isfile(file_name):
                    print(file_name)
        elif cmd == 'down':
            print(download(int(op[0])))
        elif cmd == 'up':
            print(upload(op[0]))
        elif cmd == 'rm':
            print(delete(int(op[0])))
        else:
            print('please input correct commend!')

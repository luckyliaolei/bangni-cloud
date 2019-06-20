import hashlib
import getopt
import os
import sys
import requests
import shutil
import threading


mate_server = 'http://127.0.0.1:5000'
chunk_size = 8 * 2 ** 20 # 8 MB


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
    s.post(mate_server + '/list', files={'file': ('haha', open('.viminfo', 'rb'))})


def upload(filename):
    r = s.get(mate_server + '/nodes')
    ips = [row['ip'] for row in r.json()]

    f = open(filename)


    md5 = hashlib.md5()
    i = 0
    for chunk in iter(lambda: f.read(chunk_size), b''):
        md5.update(chunk)
        r.post(mate_server + '/upload', files={'file': (md5.hexdigest(), chunk)})
        s.get('http://127.0.0.1:5000/chun', files={'file': ('haha', )})


def download(filename):
    #t1 = threading.Thread(target=run_thread, args=(5,))

    shutil.copyfileobj()


def delete(filename):
    s.post('http://127.0.0.1:5000/delete', data={'filename': filename})


def login(name, passwd):
    s = requests.session()
    r = s.get('/login', params={'name': name, 'passwd': passwd})
    r = r.json()
    if r['res']:
        return s
    else:
        print(r['msg'])
        return False


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

    while True:
        line = input()
        cmd, *op = line.split(' ')
        if cmd == 'q':
            sys.exit(0)
        elif cmd == 'ls':
            list_file()
        elif cmd == 'down':
            download(op[1])
        elif cmd == 'up':
            upload(op[0])
        elif cmd == 'rm':
            delete(op[0])
        else:
            print('please input correct commend!')





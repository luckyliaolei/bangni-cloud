import hashlib
import getopt
import os
import sys
import requests
import shutil
import threading



chunk_size = 8 * 1024 * 1024


def usage():
    u = '''
    Name:
        %s - dayu wechat alert message send interface

    Synopsis:
        %s [-h] [-u] [-s]
    Description:
        Arguments are as following
            -h  print this help message
            -p  user to send
            -s  alert message to send
    '''
    prog = os.path.basename(sys.argv[0])
    print(u % (prog, prog))
    sys.exit(0)

def list_file():
    requests.post('http://127.0.0.1:5000/', files={'file': ('haha', open('.viminfo', 'rb'))})


def upload(filename):
    f = open(filename)
    hashs = []
    for chunk in iter(lambda: f.read(chunk_size), b''):
        hashs.append(hashlib.md5(chunk).hexdigest())
        requests.post('http://127.0.0.1:5000/upload', files={'file': ('haha', open('.viminfo', 'rb'))})


def download(filename):
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    shutil.copyfileobj()

def delete(filename):
    requests.post('http://127.0.0.1:5000/upload', })

def login():
    s = requests.session()
    r = s.get('/login', params={'name': 'liao', 'passwd': 'll'})
    return r.json()

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:s:', "help")
    except getopt.GetoptError as e:
        sys.exit(1)

    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
        elif op == "-p":
            pass
        elif op == "-s":
            pass

    login()

    while True:
        line = input()
        cmd, *op = line.split(' ')
        if cmd == 'q':
            sys.exit(0)
        elif cmd == 'ls':
            list_file()
        elif cmd == 'download':
            download(op)
        elif cmd == 'upload':
            up
        elif cmd == ''




import socket
import multiprocessing
import sys
import struct
import time
from threading import Lock, Thread

list_msg = None 
my_msg = None 
name = None 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock0 = multiprocessing.Lock()
lock1 = multiprocessing.Lock()
port = -1

def sync(index, list_addr):
    global list_msg

    list_addr = list_addr.split('|')
    list_addr.pop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for _addr in list_addr:
        _addr = _addr.split('_')
        if not (int(_addr[1]) == port):
            print('Sync with ', end ="")
            print(_addr[0], _addr[1])
            sock.connect((_addr[0], int(_addr[1]))) 
            sock.send(bytes(str(index), "utf-8"))
            msg = sock.recv(1024).decode("utf-8")
            if(msg == '-1'):
                continue
            else:
                print(msg)
                return msg
        
def serverFlow():
    global list_msg
    global my_msg

    my_index = -1
    svr_index = -2

    while True:
        time.sleep(0.5)
        sock.send(b'LASTMSG')
        svr_index = int(sock.recv(1024).decode("utf-8"))

        while(my_index < svr_index):
            my_index += 1
            if not(my_index in my_msg):
                _str = 'GET_'+str(my_index)
                
                lock1.acquire()
                sock.send(bytes(_str, 'utf-8'))
                msg = sock.recv(1024).decode("utf-8")
                lock1.release()

                msg = sync(my_index, msg)
                lock0.acquire()
                list_msg[my_index] = msg
                lock0.release()

                lock1.acquire()
                sock.send(bytes('SYNC_'+str(my_index), 'utf-8'))
                lock1.release()

def getMsg(sock_cli, addr_cli):
    global list_msg

    index = int(sock_cli.recv(1024).decode("utf-8"))
    if not(index in list_msg):
        msg = '-1'
    else: 
        msg = list_msg[index]
    sock_cli.send(bytes(msg, "utf-8"))

def newConnection():
    global list_msg
    sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_cli.bind(('localhost', port))
    sock_cli.listen(1)

    while True:
        con, cliente = sock_cli.accept()
        multiprocessing.Process(target=getMsg, args=(con, cliente,)).start()

if __name__ == '__main__':
    list_msg = dict()
    my_msg = []

    name = sys.argv[1]
    port = int(sys.argv[2])

    #multiprocessing.Process(target=newConnection).start()
    Thread(target=newConnection).start()

    sock.connect(('localhost', 40006))
    sock.send(bytes(str(port), 'utf-8'))

    Thread(target=serverFlow).start()
    #multiprocessing.Process(target=serverFlow).start()

    while(True):
        msg = input()
        lock1.acquire()
        sock.send(b'SEND_')
        index = int(sock.recv(1024).decode("utf-8"))
        my_msg.append(index)
        lock1.release()

        lock0.acquire()
        list_msg[index] = str(name+'> '+msg)
        lock0.release()
    
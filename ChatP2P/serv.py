import socket
import multiprocessing
import sys
import struct
from threading import Lock, Thread

list_msg = []
lock = Lock()
cli_sock = dict()

def clientFlow(sock_cli, addr_cli):
    global list_msg
    msg = sock_cli.recv(1024).decode("utf-8")
    cli_sock[addr_cli] = int(msg)
    while True:
        msg = sock_cli.recv(1024).decode("utf-8")

        msg = msg.split('_')
        lock.acquire()
        if(msg[0] == 'LASTMSG'):
            sock_cli.send(bytes(str(len(list_msg) - 1), 'utf-8'))
        elif(msg[0] == 'SEND'):
            sock_cli.send(bytes(str(len(list_msg)), "utf-8"))
            v = []
            v.append(str(addr_cli[0])+'_'+str(cli_sock[addr_cli]))
            list_msg.append(v)
            print(list_msg)
        elif(msg[0] == 'GET'):
            print('----> GETTT!')
            index = int(msg[1])
            rmsg = ''
            for a in list_msg[index]:
                rmsg += a + '|'
            sock_cli.send(bytes(rmsg, 'utf-8'))
            print(list_msg)
        elif(msg[0] == 'SYNC'):
            index = int(msg[1])
            list_msg[index].append(str(addr_cli[0])+'_'+str(cli_sock[addr_cli]))
            print(list_msg)
        lock.release()

def newConnection():
    con, cliente = sock.accept()
    print(con)

    #multiprocessing.Process(target=clientFlow, args=(con, cliente,)).start()
    Thread(target=clientFlow,args=(con, cliente,)).start()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 40006))
    sock.listen(1)
    while True:
        newConnection()


'''
import time
import multiprocessing

def deposit(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value + 1
        lock.release()

def withdraw(balance, lock):
    for i in range(100):
        time.sleep(0.01)
        lock.acquire()
        balance.value = balance.value - 1
        lock.release()

if __name__ == '__main__':
    balance = multiprocessing.Value('i', 200)
    lock = multiprocessing.Lock()
    d = multiprocessing.Process(target=deposit, args=(balance,lock))
    w = multiprocessing.Process(target=withdraw, args=(balance,lock))
    d.start()
    w.start()
    d.join()
    w.join()
    print(balance.value)
'''
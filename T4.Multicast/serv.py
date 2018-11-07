#servudir
import socket
import thread
import sys
import struct

dict_addr_name = dict()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.100.7', 40006))
sock.listen(1)

def recv_from_client(sock_cli, addr_cli):
    fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    name = sock_cli.recv(1024)
    dict_addr_name[addr_cli] = name
    print 'NEW  ', addr_cli[0],addr_cli[1],name
    fd.sendto('**' + name + ' entrou no chat**', ('224.1.1.1', 5007))

    while True:
        msg = sock_cli.recv(1024)
        if not msg: break
        fd.sendto(dict_addr_name[addr_cli] + '> ' + msg, ('224.1.1.1', 5007))

    print 'CLOSE', addr_cli[0],addr_cli[1],name
    fd.sendto('**' +dict_addr_name[addr_cli]+' saiu do chat**', ('224.1.1.1', 5007))
    sock_cli.close()
    thread.exit()


while True:
    con, cliente = sock.accept()
    thread.start_new_thread(recv_from_client, tuple([con, cliente]))

sock.close()

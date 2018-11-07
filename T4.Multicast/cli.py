import socket
import sys
import thread
import struct

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

quit = False
name = ''
def writeBuffer(addr, port):
    MCAST_GRP = addr
    MCAST_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while not quit:
        msg = sock.recv(1024)
        if(msg.split('>')[0] != name):
            print msg

    thread.exit()

name = sys.argv[1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.100.7', 40006))
sock.send (name)

thread.start_new_thread(writeBuffer, tuple(['224.1.1.1', 5007]))
while not quit:
    msg = raw_input()
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)

    if(msg == 'quit'):
        quit = True
        break

    print 'eu> ' + msg
    sock.send(msg)

sock.close()

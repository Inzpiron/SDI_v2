import socket

UDP_IP   = '192.168.100.7'
UDP_PORT = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(2000000)
    print "received message: ", len(data)


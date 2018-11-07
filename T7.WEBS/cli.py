import pika
import os
import sys
from zeep import Client
from time import sleep


client = Client('http://192.168.100.7:9876/WSHello?wsdl')
myid = 0
myname = sys.argv[1]

def send():
    while True:
        msg = input()
        client.service.enviarMensagem(myid, msg)

if __name__ == '__main__':
    myid = client.service.iniciarConexao(myname)
    newpid = os.fork()
    if(newpid == 0):
        while True:
            sleep(0.3)
            msg = client.service.getMensagem(myid)
            if msg != None:
                print(msg, end='')

    else:
        send()

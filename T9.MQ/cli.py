import pika
import os
import sys

credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters('sdi02', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
my_queue = ''
name = sys.argv[1]

def callback(ch, method, properties, body):
    body = body.decode().split('|')
    if(body[0] != my_queue):
        print(body[1])

def send():
    while True:
        try:
            message = my_queue + '|' + name + '> ' + input()
            channel.basic_publish(exchange='logs', routing_key='', body=message)
        except:
            connection.close()
            break

if __name__ == '__main__':
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result   = channel.queue_declare(exclusive=True)
    my_queue = result.method.queue
    channel.queue_bind(exchange='logs', queue=my_queue)

    channel.basic_consume(callback, queue=my_queue, no_ack=True)

    newpid = os.fork()
    if(newpid == 0):
        channel.start_consuming()
    else:
        send()

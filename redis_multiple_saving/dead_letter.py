import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='dlx', exchange_type='direct')

result = channel.queue_declare(queue='dl')
queue_name = result.method.queue
channel.queue_bind(exchange='dlx',
                   routing_key='dl', # x-dead-letter-routing-key
                   queue=queue_name)

print(' [*] Waiting for dead-letters. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print (" [x] %r" % (properties,))
    print (" [reason] : %s : %r" % (properties.headers['x-death'][0]['reason'], body))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(queue='dl', on_message_callback=callback, auto_ack=False)

channel.start_consuming()
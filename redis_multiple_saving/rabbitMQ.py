import pika
from redis_multiple_saving.consumer import callback

# Creating connection and channel with localhost RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Creating a new Exchange and Queue
channel.exchange_declare(exchange='save_on_redis_exchange', exchange_type='fanout')
channel.queue_declare(queue='save_on_redis_queue',
                      arguments={
                          'x-message-ttl': 1000,
                          "x-dead-letter-exchange": "dlx",
                          "x-dead-letter-routing-key" : "dl", # if not specified, queue's routing-key is used
                      })

# Binding my Queue into Exchange
channel.queue_bind(exchange='save_on_redis_exchange', queue='save_on_redis_queue')

# Start consuming
print('[*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(queue='save_on_redis_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
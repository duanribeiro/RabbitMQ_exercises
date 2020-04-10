import pika
from datetime import datetime
import json
import time
import random


# Creating connection and channel with localhost RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

for iteration in range(10):
    # Simulating some process time
    string_time = datetime.now().time().strftime("%H:%M:%S")
    random_value = random.randrange(3)
    time.sleep(random_value)

    x = channel.basic_publish(exchange='save_on_redis_exchange',
                          routing_key='',
                          body=json.dumps({
                              "producer": "producer_1",
                              "time": string_time,
                              "random_value": random_value
                          }))

connection.close()
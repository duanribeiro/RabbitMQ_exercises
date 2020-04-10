import json
from datetime import datetime


def callback(ch, method, properties, body):
    body = json.loads(body.decode())

    print(f"{datetime.now().time().strftime('%H:%M:%S.%f')}")
    print(f"{body['producer']} -- {body['time']}  -- {body['random_value']}")

    if body['random_value'] % 2 == 0:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
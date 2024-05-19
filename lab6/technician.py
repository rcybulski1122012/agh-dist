import json

import pika
import sys

from pika.exchange_type import ExchangeType

from lab6.common import ExaminationType, HOST, REQUEST_EXCHANGE_NAME, RESPONSE_EXCHANGE_NAME, QUEUE_NAMES

TECHNICIAN_NAME = sys.argv[1]
SUPPORTED_EXAMINATIONS = [ExaminationType(examination) for examination in sys.argv[2].split(",")]

parameters = pika.ConnectionParameters(HOST)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange=REQUEST_EXCHANGE_NAME, exchange_type=ExchangeType.direct)
channel.exchange_declare(exchange=RESPONSE_EXCHANGE_NAME, exchange_type=ExchangeType.direct)


def handle_examination(_channel, _method, _properties, body) -> None:
    message = json.loads(body.decode())
    patient_name = message["patient_name"]
    examination = message["examination"]
    doctor_name = message["doctor_name"]

    print(f"{TECHNICIAN_NAME} is examining {patient_name}'s {examination}")

    response_message = f"{patient_name} {examination} done"
    channel.basic_publish(exchange=RESPONSE_EXCHANGE_NAME, routing_key=doctor_name, body=response_message)


for supported_examination in SUPPORTED_EXAMINATIONS:
    queue_name = QUEUE_NAMES[supported_examination]
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=REQUEST_EXCHANGE_NAME, queue=queue_name, routing_key=supported_examination)
    channel.basic_consume(queue=queue_name, on_message_callback=handle_examination, auto_ack=True)


channel.start_consuming()
connection.close()

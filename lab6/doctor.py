import json
import sys
import threading
import pika

from lab6.common import ExaminationType, HOST, REQUEST_EXCHANGE_NAME, RESPONSE_EXCHANGE_NAME

DOCTOR_NAME = sys.argv[1]
RESPONSE_QUEUE = f"{DOCTOR_NAME}-queue"

parameters = pika.ConnectionParameters(HOST)


def callback(_chanel, _method, _properties, body):
    message = body.decode()
    print(f"Received message: {message}")


def send_requests():
    connection_send = pika.BlockingConnection(parameters)
    channel_send = connection_send.channel()

    while True:
        patient_name = input("Enter patient name: ")
        try:
            patient_examination = ExaminationType(input("Enter patient examination (knee, hip or elbow): "))
        except ValueError:
            print("Invalid examination type")
            continue

        message = json.dumps({
            "patient_name": patient_name,
            "examination": patient_examination.value,
            "doctor_name": DOCTOR_NAME
        })
        channel_send.basic_publish(exchange=REQUEST_EXCHANGE_NAME, routing_key=patient_examination, body=message)

    connection_send.close()


sender_thread = threading.Thread(target=send_requests)
sender_thread.start()

connection_receive = None
try:
    connection_receive = pika.BlockingConnection(parameters)
    channel_receive = connection_receive.channel()

    channel_receive.queue_declare(queue=RESPONSE_QUEUE)
    channel_receive.queue_bind(queue=RESPONSE_QUEUE, exchange=RESPONSE_EXCHANGE_NAME, routing_key=DOCTOR_NAME)
    channel_receive.basic_consume(queue=RESPONSE_QUEUE, on_message_callback=callback, auto_ack=True)

    channel_receive.start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    if connection_receive:
        connection_receive.close()

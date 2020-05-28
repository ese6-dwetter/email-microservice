import json
import os
import pika

from dotenv import load_dotenv
from python_json import *
from mail_builder import (
    send_welcome_mail,
    send_verification_mail,
)

load_dotenv()

# Load parameters
parameters = pika.ConnectionParameters(
    host=os.getenv("MESSAGE_QUEUE_HOST"),
    port=int(os.getenv("MESSAGE_QUEUE_PORT")),
    credentials=pika.PlainCredentials(
        username=os.getenv("MESSAGE_QUEUE_USERNAME"),
        password=os.getenv("MESSAGE_QUEUE_PASSWORD")
    )
)

# Setup AMQP connection with parameters
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_bind(exchange="Dwetter", queue="EmailMicroservice")


# Create callback function
def callback(ch, method, properties, body):
    print("Method: {}".format(method))
    print("Properties: {}".format(properties))
    data = eval(json.loads(body))
    print("Body: {}".format(data))

    # Send the corresponding email of the MessageType header
    message_type = properties.headers['MessageType']
    if message_type == "RegisterUser":
        send_welcome_mail(data['Email'], data['Username'])
    elif message_type == "VerifyEmail":
        send_verification_mail(data['Email'], data['Username'])


channel.basic_consume(
    queue="EmailMicroservice",
    on_message_callback=callback,
    auto_ack=True
)

print("[*] Start consuming...")
channel.start_consuming()

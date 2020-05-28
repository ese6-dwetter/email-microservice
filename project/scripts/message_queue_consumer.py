import json
import logging
import os
import pika

# Make sure null = None, true = True and false = False
from project.scripts.python_json import *

from project.scripts.mail_builder import (
    send_welcome_mail,
    send_verification_mail,
)


def setup_amqp_connection(exchange, queue):
    """
    Setup AMQP connection via Pika
    :param exchange: The exchange to consume from
    :param queue: The queue to consume from
    :return: AMQP connection channel
    """
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

    channel.queue_bind(exchange=exchange, queue=queue)

    return channel


def callback(ch, method, properties, body):
    logging.info("[*] A new message is received")
    logging.info("Method: {}".format(method))
    logging.info("Properties: {}".format(properties))
    data = eval(json.loads(body))
    logging.info("Body: {}".format(data))

    # Send the corresponding email of the MessageType header
    message_type = properties.headers['MessageType']
    if message_type == "RegisterUser":
        send_welcome_mail(data['Email'], data['Username'])
    elif message_type == "VerifyEmail":
        send_verification_mail(data['Email'], data['Username'])
    else:
        logging.warning("[*] The MessageType header '{}' does not exist.".format(message_type))


def start_consumer(exchange, queue):
    """
    Start the consumer with basic consume
    :param exchange: The exchange to consume from
    :param queue: The queue to consume from
    :return: None
    """
    channel = setup_amqp_connection(exchange, queue)

    channel.basic_consume(
        queue=queue,
        on_message_callback=callback,
        auto_ack=True
    )

    logging.info("[*] Start consuming...")
    channel.start_consuming()

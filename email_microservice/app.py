import logging

from dotenv import load_dotenv
from email_microservice.scripts.message_queue_consumer import start_consumer


def run():
    load_dotenv()

    logging.basicConfig(filename="app.log", level=logging.INFO)

    start_consumer("Dwetter", "EmailMicroservice")

from dotenv import load_dotenv

from message_queue_consumer import start_consumer

if __name__ == '__main__':
    load_dotenv()
    start_consumer("Dwetter", "EmailMicroservice")

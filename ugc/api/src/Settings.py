from os import getenv

from dotenv import load_dotenv
env_path = '.env'
load_dotenv(dotenv_path=env_path)


class KafkaSet:
    KAFKA_TOPIC = getenv('KAFKA_TOPIC', 'Events')
    KAFKA_HOST = getenv('KAFKA_HOST', '127.0.0.1')
    KAFKA_PORT = getenv('KAFKA_PORT', 9092)
    GROUP_ID = "echo-messages"
    CONSUMER_TIMEOUT_MS = 100
    MAX_RECORDS_PER_CONSUMER = 100

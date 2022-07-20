from os import getenv

from dotenv import load_dotenv
env_path = '.env'
load_dotenv(dotenv_path=env_path)

class KafkaSet:
    KAFKA_TOPIC = getenv('KAFKA_TOPIC', 'events')
    KAFKA_HOST = "127.0.0.1"# getenv('KAFKA_HOST', 'broker')
    KAFKA_PORT = getenv('KAFKA_PORT', 9092)

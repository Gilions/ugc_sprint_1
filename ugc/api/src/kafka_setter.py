import logging
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

from Settings import KafkaSet

logger = logging.getLogger(__name__)

producer = KafkaProducer(bootstrap_servers=[f'{KafkaSet.KAFKA_HOST}:{KafkaSet.KAFKA_PORT}'])


def create_topic() -> None:

    admin_client = KafkaAdminClient(
        bootstrap_servers=f"{KafkaSet.KAFKA_HOST}:{KafkaSet.KAFKA_PORT}",
        client_id='test'
    )

    # check if topic exists
    topic_metadata = admin_client.list_topics()
    if KafkaSet.KAFKA_TOPIC not in topic_metadata:
        try:
            topic_list = [(NewTopic(name=KafkaSet.KAFKA_TOPIC, num_partitions=1, replication_factor=1))]
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            logger.warning(f'topic {KafkaSet.KAFKA_TOPIC} created')
        except Exception as e:
            logger.exception(e)
    else:
        logger.warning(f'topic {KafkaSet.KAFKA_TOPIC} already exists')


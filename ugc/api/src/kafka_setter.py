import asyncio
import json
import logging

from fastapi import HTTPException
from http import HTTPStatus

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from models import UserValues
from Settings import KafkaSet

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


def kafka_json_deserializer(serialized):
    return json.loads(serialized)


# creating topic using kafka-python
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


async def process_load_kafka(key, value):
    producer = AIOKafkaProducer(bootstrap_servers=[f'{KafkaSet.KAFKA_HOST}:{KafkaSet.KAFKA_PORT}'])
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait(KafkaSet.KAFKA_TOPIC, key=key, value=value)
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await producer.stop()
        return {}


async def process_get_messages():
    consumer = AIOKafkaConsumer(
                                KafkaSet.KAFKA_TOPIC,
                                loop=loop,
                                bootstrap_servers=[f'{KafkaSet.KAFKA_HOST}:{KafkaSet.KAFKA_PORT}'],
                                group_id=KafkaSet.GROUP_ID,
                                enable_auto_commit=True,
                                auto_commit_interval_ms=KafkaSet.CONSUMER_TIMEOUT_MS,
                                auto_offset_reset="earliest",
                                value_deserializer=kafka_json_deserializer,
        )

    await consumer.start()
    retrieved_requests = []
    try:

        result = await consumer.getmany(
            timeout_ms=KafkaSet.CONSUMER_TIMEOUT_MS, max_records=KafkaSet.MAX_RECORDS_PER_CONSUMER
        )
        for tp, messages in result.items():
            if messages:
                for message in messages:
                    retrieved_requests.append(UserValues(key=message.key.decode("utf-8"),
                                                         value=json.dumps(message.value)))

            else:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Kafka messages not found")

    except Exception as e:
        logger.error(f"Error when trying to consume : {str(e)}")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    finally:
        await consumer.stop()

    return retrieved_requests

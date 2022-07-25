import json
from typing import List
from fastapi import APIRouter

from models.models import Event, UserValues
from service.kafka_setter import process_load_kafka, process_get_messages


router = APIRouter()

@router.post("/ugc-producer",
          summary='Прием аналитических данных',
          description='Сбор данных от пользователя',
          tags=['UGC'],
          status_code=204)
async def kafka_load(event: Event):
    """
    Produce a test ugc messages into kafka.
    """
    key = json.dumps(str(event.user_id) + event.movie_id).encode()
    my_info = json.dumps(event.dict()).encode()
    return await process_load_kafka(key=key, value=my_info)


@router.get("/ugc-consumer",
          response_model=List[UserValues],
          summary='Получение данных из хранилища',
          description='Проверка работы хранилища Kafka',
          tags=['UGC'],
          status_code=200)
async def get_messages_from_kafka():
        """
        Consume a list of messages from kafka.
        """

        return await process_get_messages()

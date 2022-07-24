import asyncio
import json
import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from typing import List

from kafka_setter import create_topic, process_load_kafka, process_get_messages
from models import Event, UserValues


logger = logging.getLogger(__name__)

app = FastAPI(title="UGC",
    description='Асинхронный сборщик UGC',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,)


@app.on_event("startup")
def startup_event():
    create_topic()


@app.post("/ugc-producer",
          summary='Прием аналитических данных',
          description='Сбор данных от пользователя',
          tags=['UGC'],
          status_code=204)
async def kafka_load(event: Event):
    """
    Produce a test ugc messages into kafka.
    """
    key = json.dumps(event.user_id + event.movie_id).encode()
    my_info = json.dumps(event.dict()).encode()
    return await process_load_kafka(key=key, value=my_info)


@app.get("/ugc-consumer",
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

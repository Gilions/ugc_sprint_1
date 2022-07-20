import json
import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from kafka_setter import create_topic, producer
from models import Event
from Settings import KafkaSet


logger = logging.getLogger(__name__)

app = FastAPI(title="UGC",
    description='Асинхронный сборщик UGC',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,)


@app.on_event("startup")
def startup_event():
    create_topic()


@app.post("/ugc-receiver",
          summary='UGC API',
          description='Сбор данных от пользователя',
          status_code=204)
def kafka_load(event: Event):
    try:
        key = json.dumps(event.user_id + event.movie_id).encode()
        my_info = json.dumps(event.dict()).encode()
        producer.send(KafkaSet.KAFKA_TOPIC, key=key, value=my_info)
    except Exception as exc:
        logger.exception(exc)
    return {}

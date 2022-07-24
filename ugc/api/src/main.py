import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import kafka_producer
from service.kafka_setter import create_topic


logger = logging.getLogger(__name__)

app = FastAPI(title="UGC",
    description='Асинхронный сборщик UGC',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,)


@app.on_event("startup")
def startup_event():
    create_topic()


app.include_router(kafka_producer.router, prefix='/api/v1/kafka')


FROM python:3.9-alpine3.15

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY ./app .

RUN addgroup -S web && adduser -S web -G web \
    && chown web:web -R /app
USER web

COPY ./entrypoint.sh .
ENTRYPOINT ["sh", "/entrypoint.sh"]
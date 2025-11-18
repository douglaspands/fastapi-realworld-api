FROM python:3.13-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /fastapi-realworld-api

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

ADD ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations
COPY ./app ./app

EXPOSE 80

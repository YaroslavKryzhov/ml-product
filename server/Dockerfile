FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /server

RUN apt-get update \
  && apt-get -y install netcat gcc python-dev postgresql libpq-dev \
  && apt-get clean

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
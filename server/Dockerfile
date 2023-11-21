FROM amd64/python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 netcat gcc python-dev postgresql libpq-dev -y
RUN apt-get clean


RUN python -m pip --no-cache-dir install --upgrade pip
RUN python -m pip install poetry && \
    poetry config virtualenvs.create false

WORKDIR /server

COPY pyproject.toml poetry.lock ./

RUN poetry install
#RUN poetry run poe catboost_install
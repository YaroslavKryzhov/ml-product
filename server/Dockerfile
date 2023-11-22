FROM amd64/python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip --no-cache-dir install --upgrade pip
RUN python -m pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.path /virtualenv && \
    poetry config virtualenvs.in-project false

WORKDIR /server

COPY pyproject.toml poetry.lock ./

RUN poetry install
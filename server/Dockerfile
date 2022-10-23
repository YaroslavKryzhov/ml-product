FROM amd64/python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /server

#RUN apt-get update \
#  && apt-get -y install netcat gcc python-dev postgresql libpq-dev \
#  && apt-get clean

RUN pip install --upgrade pip
#RUN pip install --upgrade setuptools
#RUN pip install catboost
#RUN pip install xgboost
#RUN pip install lightgbm

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
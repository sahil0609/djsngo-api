from python:3.7-alpine

ENV PYTHONUNBUFFERED 1
COPY ./dependancy.txt /dependancy.txt
RUN pip install -r /dependancy.txt
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D sahil
USER sahil


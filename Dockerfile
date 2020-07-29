from python:3.7-alpine

ENV PYTHONUNBUFFERED 1
COPY ./dependancy.txt /dependancy.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp_build gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /dependancy.txt
RUN apk del  .tmp_build
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D sahil
USER sahil


FROM python:3.8-alpine

WORKDIR /app

COPY /scripts ./

ENTRYPOINT [ "python", "consumer.py" ]
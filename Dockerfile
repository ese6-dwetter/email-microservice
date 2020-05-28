FROM python:3.8-alpine

WORKDIR /app

COPY /requirements.txt /

RUN pip install -r ./requirements.txt

COPY /email_microservice /email_microservice

ENTRYPOINT [ "python", "-m", "email_microservice" ]

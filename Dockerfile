FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY email_microservice/ ./email_microservice/

ENTRYPOINT [ "python", "-m", "email_microservice" ]

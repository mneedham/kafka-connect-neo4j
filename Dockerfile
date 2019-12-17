FROM twint:alpine

MAINTAINER x0rzkov@protonmail.com

RUN apk add --no-cache librdkafka-dev gcc nano bash

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app/

RUN pip3 install -r requirements.txt

COPY twint-graph.py /opt/app/twint-graph.py
COPY docker-entrypoint.sh /opt/app/entrypoint.sh

ENTRYPOINT ["python", "twint-graph.py"]

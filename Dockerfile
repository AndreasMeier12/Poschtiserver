# syntax=docker/dockerfile:1

FROM python:3.8-alpine3.15

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apk add build-base py3-gunicorn libffi-dev && pip3 install -r requirements.txt && apk del build-base


COPY . .

EXPOSE 5000



CMD [ "gunicorn", "--bind" , "0.0.0.0:5000", "poschtiserver:app"]
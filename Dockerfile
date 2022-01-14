# syntax=docker/dockerfile:1

FROM python:3.8-alpine3.15

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apk add build-base
RUN apk add py3-gunicorn
RUN apk add libffi-dev

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000



CMD [ "gunicorn", "--bind" , "0.0.0.0:5000", "poschtiserver:app"]
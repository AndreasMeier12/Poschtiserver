# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install default-libmysqlclient-dev
RUN apt-get -y install gunicorn

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000



CMD [ "gunicorn", "--bind" , "0.0.0.0:5000", "poschtiserver:app"]
FROM python:3.10.7-slim-buster

RUN apt -y update && apt -y upgrade  && apt -y install sqlite3 && rm -rf /var/lib/apt/lists/*

COPY taskpool/audio-generated ./taskpool/audio-generated
COPY taskpool/taskpool.db ./taskpool/taskpool.db

WORKDIR /taskpool
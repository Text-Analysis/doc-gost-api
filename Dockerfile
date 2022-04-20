# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app ./app

ENV URI="${URI}"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]
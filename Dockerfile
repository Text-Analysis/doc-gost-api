FROM python:3.8

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

ENV URI="${URI}"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]
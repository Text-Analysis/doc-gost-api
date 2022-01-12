FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV URI="${URI}"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload"]
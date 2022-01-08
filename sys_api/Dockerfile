FROM python:3.8-slim-buster

WORKDIR /api

COPY requirements.txt /api/requirements.txt

RUN apt-get update && apt-get -y install sudo

RUN sudo apt-get -y install gcc

RUN sudo apt-get update && sudo apt-get -y install libmariadb-dev

COPY webapp /api/webapp

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "webapp.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

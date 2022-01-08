FROM python:3.8-slim-buster

WORKDIR /webapp

COPY requirements.txt /webapp/requirements.txt

RUN apt-get update && apt-get -y install sudo

RUN sudo apt-get -y install gcc

RUN sudo apt-get update && sudo apt-get -y install libmariadb-dev

COPY webapp /webapp/webapp
COPY instance /webapp/instance

RUN pip3 install -r requirements.txt

ENV FLASK_APP=webapp
ENV FLASK_ENV=development
CMD ["flask", "run"]

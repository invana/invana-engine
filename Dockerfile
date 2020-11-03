# 28, June 2017
# =====================

FROM python:3.7
MAINTAINER Ravi RT Merugu <rrmerugu@gmail.com>
ENV PYTHONUNBUFFERED 1

ARG GREMLIN_SERVER_URL
ENV GREMLIN_SERVER_URL ${GREMLIN_SERVER_URL}

# create webapp folder in the container
RUN [ -d /webapp ] || mkdir /webapp;
COPY ./webapp/ /webapp
WORKDIR /webapp

# install the requirements
RUN pip install pipenv
RUN pipenv install
EXPOSE 8000

# fire it up ...
CMD  uvicorn invana.start_server:app --port 8000

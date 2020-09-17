# 28, June 2017
# =====================

FROM python:3.7
MAINTAINER Ravi RT Merugu <rrmerugu@gmail.com>
ENV PYTHONUNBUFFERED 1

ARG build_env
ARG gremlin_server_url
ENV BUILD_ENV ${build_env}
ENV GREMLIN_SERVER_URL ${gremlin_server_url}

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

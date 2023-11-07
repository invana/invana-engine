FROM python:3.8.5
MAINTAINER Ravi RT Merugu <rrmerugu@gmail.com>
ENV PYTHONUNBUFFERED 1

ARG GRAPH_BACKEND_URL
ENV GRAPH_BACKEND_URL ${GRAPH_BACKEND_URL}

# create webapp folder in the container
RUN [ -d /webapp ] || mkdir /webapp;
COPY ./ /webapp
COPY ./Pipfile /webapp
COPY ./Pipfile.lock /webapp
WORKDIR /webapp
# install the requirements
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install 
EXPOSE 8200
# fire it up ...
CMD pipenv run uvicorn invana_engine.server.app:app  --loop=asyncio  --port=8200

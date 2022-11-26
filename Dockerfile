FROM python:3.8.5
MAINTAINER Ravi RT Merugu <rrmerugu@gmail.com>
ENV PYTHONUNBUFFERED 1

ARG GREMLIN_SERVER_URL
ENV GREMLIN_SERVER_URL ${GREMLIN_SERVER_URL}

# create webapp folder in the container
RUN [ -d /webapp ] || mkdir /webapp;
COPY ./ /webapp
COPY ./Pipfile /webapp
COPY ./Pipfile.lock /webapp
WORKDIR /webapp
# install the requirements
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN pip install -r prod-requirements.txt
EXPOSE 8200
# fire it up ...
#CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8200  invana_engine.server_start:app
CMD uvicorn invana_engine.server.app:app  --loop=asyncio

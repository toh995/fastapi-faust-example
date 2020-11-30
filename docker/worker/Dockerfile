# this image has both python and rocksDB installed
FROM toh995/rocksdb-python:6.14.5_3.8.6-slim-buster

WORKDIR /fastapi-faust-example

# install pipenv packages
RUN pip install pipenv==2020.11.15

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system --deploy

# uninstall pipenv
RUN pip install pip-autoremove==0.9.1
RUN pip-autoremove pipenv -y
RUN pip uninstall pip-autoremove -y

RUN rm Pipfile Pipfile.lock

# install python-rocksdb
ARG ROCKSDB_DEPENDENCIES="g++ libbz2-dev liblz4-dev libsnappy-dev libz-dev"

RUN apt-get update \
  && apt-get install -y $ROCKSDB_DEPENDENCIES \
  && rm -rf /var/lib/apt/lists/*

RUN pip install python-rocksdb==0.7.0

# set up the wait script
RUN apt-get update \
  && apt-get install -y netcat \
  && rm -rf /var/lib/apt/lists/*

COPY bin/wait-for/ ./bin/wait-for/
RUN chmod u+x ./bin/wait-for/wait-for.sh

# copy source files
COPY app ./app

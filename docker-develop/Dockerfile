FROM python:3.6-slim
COPY docker-develop/requirements.txt /srv/requirements.txt

WORKDIR /srv

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 libcairo2-dev  libpangocairo-1.0-0
RUN pip install -r /srv/requirements.txt --no-cache-dir

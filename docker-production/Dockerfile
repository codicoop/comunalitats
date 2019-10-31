root@vps001:/srv/Coopolis.back-office/docker-production# cat Dockerfile
FROM python:3.6-alpine
COPY docker/requirements.txt /srv/requirements.txt

WORKDIR /srv

RUN pip install --upgrade pip
RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add jpeg-dev zlib-dev py-pillow
RUN apk add postgresql-dev
RUN apk add --no-cache libffi-dev
RUN pip install -r /srv/requirements.txt
# Weasyprint installation for Alpine:
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
# Installing font for PDFs:
RUN apk --update add fontconfig ttf-opensans
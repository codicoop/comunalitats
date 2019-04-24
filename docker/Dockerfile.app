FROM python:3.6-alpine
COPY Coopolis.back-office/requirements.txt /srv/requirements.txt

WORKDIR /srv

RUN pip install --upgrade pip
RUN apk update 
RUN apk add --virtual build-deps gcc python3-dev musl-dev 
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev 
RUN apk add jpeg-dev zlib-dev py-pillow 
RUN apk add postgresql-dev
RUN apk add --no-cache libffi-dev
RUN pip install -r /srv/requirements.txt

# ENV DJANGO_SETTINGS_MODULE="coopolis_backoffice.settings.prod"
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "coopolis_backoffice.wsgi:application"]

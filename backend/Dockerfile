FROM python:3.8

RUN apt-get update -y
RUN apt-get install binutils libproj-dev gdal-bin cron -y

COPY ./conf/requirements.txt /
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r ./requirements.txt

WORKDIR /opt/
EXPOSE 8000
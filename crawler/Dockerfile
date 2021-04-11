
FROM python:3.8

RUN apt update -y && apt upgrade -y \
	&& apt -y install python3-pip vim curl supervisor less \
	&& apt clean
RUN pip3 install flask gunicorn pytz
RUN pip3 install python-twitter google-cloud-bigquery
# RUN pip3 install mecab-python3 emoji

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

CMD exec gunicorn --bind :8080 --workers 1 --threads 2 app:app

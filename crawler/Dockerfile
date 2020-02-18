
FROM python:3.8

RUN apt update -y && apt upgrade -y && \
	apt -y install python3-pip vim curl supervisor less \
	mecab libmecab-dev mecab-ipadic-utf8 sudo && \
	apt clean
RUN pip3 install flask gunicorn
RUN pip3 install python-twitter google-cloud-bigquery
RUN pip3 install mecab-python3 emoji

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN yes "yes" | /mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -p /ipadic

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

CMD exec gunicorn --bind :8080 --workers 1 --threads 2 app:app

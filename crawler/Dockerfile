
FROM python:3.5

RUN apt-get update -y && apt-get upgrade -y && \
	apt-get -y install python3-pip vim curl supervisor less && \
	apt-get clean
RUN pip3 install flask gunicorn
RUN pip3 install python-twitter google-cloud-bigquery

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

CMD exec gunicorn --bind :8080 --workers 1 --threads 2 app:app

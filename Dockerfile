FROM python:3.5
MAINTAINER Abrstudio

RUN apt-get update && apt-get install -y \
	git \
	python-setuptools \
	nginx \
	supervisor \
	sqlite3 \
	libmysqlclient-dev \
	python3-dev \
  && rm -rf /var/lib/apt/lists/*
RUN easy_install pip && pip install uwsgi && echo "daemon off;" >> /etc/nginx/nginx.conf && mkdir -p /home/docker/code/

COPY ./requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt


COPY ./config/nginx-app.conf /etc/nginx/sites-available/default
COPY ./config/supervisor-app.conf /etc/supervisor/conf.d/
COPY ./ /home/docker/code/
RUN cd /home/docker/code; mv ./bazicharge/settingsDeploy.py ./bazicharge/settings.py; python manage.py collectstatic --noinput;
VOLUME ["/var/log/uwsgi/"]

EXPOSE 80
CMD ["supervisord", "-n"];
FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo nginx php7.4-fpm curl supervisor openssh-server

RUN adduser randal

# Setup filestorage site
RUN mkdir /home/randal/filestorage
COPY ./foothold /home/randal/filestorage
RUN chown -R randal:randal /home/randal/filestorage

COPY config/filestorage.conf /etc/nginx/sites-available/filestorage

RUN ln -s /etc/nginx/sites-available/filestorage /etc/nginx/sites-enabled/ && \
    unlink /etc/nginx/sites-enabled/default

EXPOSE 80

# Setup supervisord
COPY supervisord.conf /etc/supervisor/supervisord.conf

CMD mkdir -p /run/php/ && service ssh start && supervisord -c /etc/supervisor/supervisord.conf

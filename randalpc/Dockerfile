FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo nginx php7.4-fpm curl supervisor openssh-server
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 sudo

RUN adduser randal

# Setup filestorage site
RUN mkdir /home/randal/filestorage
COPY ./foothold /home/randal/filestorage
RUN chown -R randal:randal /home/randal/filestorage

COPY config/filestorage.conf /etc/nginx/sites-available/filestorage

RUN ln -s /etc/nginx/sites-available/filestorage /etc/nginx/sites-enabled/ && \
    unlink /etc/nginx/sites-enabled/default

EXPOSE 80

# Setup root part
COPY ./root/safepickle.py /usr/local/bin/safepickle
RUN chmod +x /usr/local/bin/safepickle

COPY ./root/example.safepkl /home/randal

RUN echo 'randal ALL=(ALL) NOPASSWD: /usr/local/bin/safepickle' >> /etc/sudoers

COPY ./hint.txt /root/hint.txt

RUN echo "randal:KzsRCywroBPdLrCV" | chpasswd

# Setup supervisord
COPY supervisord.conf /etc/supervisor/supervisord.conf

CMD mkdir -p /run/php/ && service ssh start && supervisord -c /etc/supervisor/supervisord.conf

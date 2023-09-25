FROM ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y sudo nginx php7.4-fpm curl supervisor

RUN adduser james

RUN mkdir /var/www/petsite
COPY data-redundancy /var/www/petsite/
RUN chown -R www-data:www-data /var/www/petsite

COPY config/php-fpm.conf /etc/php/7.4/fpm/php-fpm.conf
COPY config/petsite.conf /etc/nginx/sites-available/petsite

RUN ln -s /etc/nginx/sites-available/petsite /etc/nginx/sites-enabled/
RUN unlink /etc/nginx/sites-enabled/default

EXPOSE 80

COPY supervisord.conf /etc/supervisor/supervisord.conf

CMD supervisord -c /etc/supervisor/supervisord.conf

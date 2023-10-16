FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y sudo python3 python3-pip openssh-server build-essential gcc curl

RUN adduser hamish
RUN echo "hamish:FPawioVpxniPxuYD" | chpasswd

RUN echo 'Defaults env_keep += "HTTP_PROXY"' >> /etc/sudoers
RUN echo 'hamish ALL=(ALL) NOPASSWD: /usr/local/bin/funprogram' >> /etc/sudoers

WORKDIR /home/hamish

COPY ./root/funprogram /usr/local/bin/funprogram

CMD mkdir -p /run/sshd && /usr/sbin/sshd -D

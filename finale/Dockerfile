FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server

RUN useradd daniel
RUN echo "daniel:potentilla_hovertrain_discapacitate" | chpasswd

#TODO: add some kind of flag!

CMD mkdir -p /run/sshd && /usr/sbin/sshd -D

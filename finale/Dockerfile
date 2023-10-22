FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server sudo

RUN useradd -m daniel
RUN echo "daniel:potentilla_hovertrain_discapacitate_8204723" | chpasswd

COPY ./note.txt /home/daniel/note.txt

COPY ./flag.txt /root/flag.txt

COPY ./vuln.sh /usr/local/bin/vuln
COPY ./healthcheck.sh /usr/local/bin
RUN chmod +x /usr/local/bin/vuln /usr/local/bin/healthcheck.sh

RUN echo 'daniel ALL=(ALL) NOPASSWD: /usr/local/bin/vuln' >> /etc/sudoers

CMD mkdir -p /run/sshd && /usr/sbin/sshd -D

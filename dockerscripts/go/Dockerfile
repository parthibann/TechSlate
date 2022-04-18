FROM centos:7

MAINTAINER Parthiban Nithyanantham

USER root

RUN yum install net-tools tar wget unzip vim git epel-release pwgen -y && \
    yum repolist

WORKDIR /opt

RUN yum install -y openssl passwd sudo shellinabox --enablerepo=epel && \
    yum clean all

ENV USERPWD Tech$lat3

RUN groupadd techslate && useradd -u 5001 -g techslate -m techslate && \
    echo "$USERPWD" | passwd techslate --stdin && \
    sed -i '/pam_loginuid.so/c\#session    required     pam_loginuid.so' /etc/pam.d/login && \
    sed -i '/pam_loginuid.so/c\#session    required     pam_loginuid.so' /etc/pam.d/remote && \
    echo "techslate    ALL=(ALL)       NOPASSWD: ALL" > /etc/sudoers.d/docker

EXPOSE 4200

WORKDIR /tmp

RUN wget https://golang.org/dl/go1.16.4.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.4.linux-amd64.tar.gz
RUN echo "export PATH=/usr/local/go/bin:${PATH}" >> /root/.bashrc
RUN echo "export PATH=/usr/local/go/bin:${PATH}" >> /home/techslate/.bashrc
RUN rm -rf go1.16.4.linux-amd64.tar.gz

ADD startshell.sh /opt/startshell.sh
ADD black-on-white.css /usr/share/shellinabox/black-on-white.css

ENTRYPOINT ["/opt/startshell.sh"]
CMD ["/bin/bash"]

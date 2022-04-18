FROM centos:7

MAINTAINER Parthiban Nithyanantham

# USER root

RUN yum update -y && yum install net-tools tar wget unzip vim git epel-release python3 python3-pip pwgen -y && \
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

ADD startshell.sh /opt/startshell.sh
ADD black-on-white.css /usr/share/shellinabox/black-on-white.css

ENTRYPOINT ["/opt/startshell.sh"]
CMD ["/bin/bash"]

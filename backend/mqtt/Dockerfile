# FROM debian:jessie
FROM ubuntu:16.04

ENV MOSQUITTO_VERSION=1.4.14

# how to build the mosquitto image for V1
# install mosquitto using git-clone
# install python 2.7
# pip install pyjwt
# copy jwt python script to image
# modify pyjwt path in auth plugin
# compile mosquitto-auth-plugin locally
# copy the .so file to /mqtt

# a better way is to copy the auth-plugin source code
# from local directory into docker
# and compile it inside
# just copying a bin file is not flexible
# if this is the case
# should install python, pyjwt, <Python.h>
# specify the container path in auth-plugin Makefile (location of python.h)
# specify the path to call

RUN mkdir /zxc

COPY /backend /zxc/

RUN \
        set -x; \
        apt-get update && apt-get install -y --no-install-recommends \
                libc-ares-dev git libmysqlclient-dev libssl-dev libwebsockets-dev uuid-dev build-essential wget  ca-certificates \
                curl libcurl4-openssl-dev  libc-ares2 libcurl3 libreadline-gplv2-dev libncursesw5-dev libssl-dev\
                libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev\
        && apt-get install -y build-essential checkinstall \
        && cd /tmp \
        && wget http://mosquitto.org/files/source/mosquitto-$MOSQUITTO_VERSION.tar.gz -O mosquitto.tar.gz \
        && mkdir mosquitto-src && tar xfz mosquitto.tar.gz --strip-components=1 -C mosquitto-src \
        && cd mosquitto-src \
        && make WITH_SRV=no WITH_MEMORY_TRACKING=no \
        && make install && ldconfig \
        && mkdir /var/log/mosquitto/ \
        && wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz \
        && tar xzf Python-2.7.15.tgz \
        && rm -rf Python-2.7.15.tgz \
        && cd Python-2.7.15 \
        && ./configure --enable-optimizations \
        && make altinstall \
        && apt-get install -y python-pip \
        && pip install pyjwt \
        && pip install cryptography \
        && cd .. \
        && cp -r /zxc/mosquitto-auth-plug ./ \
        && cd mosquitto-auth-plug \
#        && sed -i "s/MOSQUITTO_SRC =/MOSQUITTO_SRC = \/tmp\/mosquitto-src\//" config.mk \
        && make \
        && cp np /var \
        && mkdir /mqtt && cp auth-plug.so /mqtt/ \
        && cp auth-plug.so /usr/local/lib/ \
        && cd examples \
        && useradd -r mosquitto \
#        && apt-get purge -y build-essential git wget ca-certificates \
#        && apt-get autoremove -y \
#        && apt-get -y autoclean \
        && rm -rf /var/cache/apt/* \
        && rm -rf  /tmp/*

VOLUME ["/var/lib/mosquitto"]

EXPOSE 1883 8883
ADD /backend/mqtt/mysql.sql /var
USER root
ADD /backend/mqtt/mosquitto.conf /etc/mosquitto/mosquitto.conf
ADD /backend/mqtt/run.sh /run.sh
RUN chmod +x /run.sh

ENTRYPOINT ["/run.sh"]
CMD ["mosquitto"]

FROM ubuntu:trusty
MAINTAINER Sangwon Lee (gamzabaw@gmail.com)

RUN apt-get update && apt-get -y install nginx

WORKDIR /etc/nginx

ENTRYPOINT ["nginx"]

EXPOSE 80
EXPOSE 443
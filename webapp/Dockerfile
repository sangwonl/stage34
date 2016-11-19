FROM ubuntu:trusty
MAINTAINER Sangwon Lee (gamzabaw@gmail.com)

RUN apt-get update \
  && apt-get install -y python python-dev python-pip python-virtualenv \
  && apt-get install -y docker.io \
  && apt-get install -y curl \
  && rm -rf /var/lib/apt/lists/*

RUN curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" > /usr/bin/docker-compose
RUN chmod +x /usr/bin/docker-compose

ENV STAGE34_HOME=/usr/stage34
ENV WEBAPP_HOME=$STAGE34_HOME/webapp

RUN mkdir temp
COPY ./requirements/* temp/
RUN pip install -r temp/dev.txt
RUN rm -rf temp

WORKDIR $WEBAPP_HOME

ENTRYPOINT ["python"]

EXPOSE 8000
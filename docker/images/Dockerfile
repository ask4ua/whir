FROM ubuntu:18.04 
WORKDIR /app
VOLUME /app 
VOLUME /data
COPY ./app/ /app/
ENV TZ=Europe/Kiev
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y python3 python3-pip python3-setuptools
RUN pip3 install mysql-connector pyyaml 
RUN pip3 install docker-py 

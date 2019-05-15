FROM ubuntu:18.04 
WORKDIR /app
VOLUME /app 
VOLUME /data
ENV TZ=Europe/Kiev
RUN apt-get update
RUN apt-get install --no-install-recommends --no-install-suggests -y git python3 python3-pip python3-setuptools python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev
RUN pip3 install mysql-connector pyyaml 
RUN pip3 install docker-py 
RUN pip3 install psycopg2
COPY ./app/ /app/

FROM ubuntu:18.04
VOLUME /app 
VOLUME /data
ENV TZ=Europe/Kiev
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y git python3 python3-pip python3-setuptools python3-dev python3-psycopg2
RUN pip3 install mysql-connector pyyaml 
RUN pip3 install docker-py 
RUN pip3 install psycopg2
COPY ./app/ /app/
CMD /app/cycle.sh
ARG version=0.0(development)
LABEL version=${version}

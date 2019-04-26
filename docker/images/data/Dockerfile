FROM whir
VOLUME /data-src
VOLUME /app-src
COPY ./app/ /app-src/
ADD ./data/SRC.tgz /data-src/
CMD cp -R /app-src/ /app/ 
CMD cp -R /data-src/ /data/ 

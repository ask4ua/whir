FROM postgres
RUN mkdir -p /run/pg_stat_tmp
RUN sed -i -e "s/^#stats_temp_directory.*$/stats_temp_directory=\'\/run\/pg_stat_tmp'/g" /var/lib/postgresql/data/postgresql.conf
COPY ./app/SQLs/upstart.sh /docker-entrypoint-initdb.d

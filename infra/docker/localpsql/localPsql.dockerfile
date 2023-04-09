FROM postgres:12
COPY ./localpsql/multi_database.sh /docker-entrypoint-initdb.d/
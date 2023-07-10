FROM postgres:15-alpine
COPY ./localpsql/multi_database.sh /docker-entrypoint-initdb.d/
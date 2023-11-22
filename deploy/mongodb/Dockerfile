FROM mongo:4.4-focal

COPY init-mongo.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init-mongo.sh

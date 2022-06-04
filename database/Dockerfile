FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root

# Scripts placed in the /docker-entrypoint-initdb.d directory will only be run if no data volume 
# exists for this container (ie: the container is being started for the first time). The scripts
# are executed in alphabetical order.
COPY sql /docker-entrypoint-initdb.d

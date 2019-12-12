#!/bin/bash
# NOTE: this naming format on different machine could be different
# if the project is not starting correctly on your machine, try the following
# cd ../
# base="${PWD##*/*/}"
# cd scripts
# echo $base
# and change the docker kill container names to "$base"_NAME_1
# if still not working, check out the acctual container names
# after docker-compose build command, and directly put them after docker kill commands

docker-compose build
docker-compose up -d
docker-compose exec --user="root" django touch /var/log/mosquitto/mosquitto.log
docker-compose run mosquitto cp /var/np /var/log/mosquitto
docker-compose run mosquitto cp /var/mysql.sql /var/log/mosquitto
docker kill v1_parser_agent_1
docker kill v1_mosquitto_1
docker kill v1_django_1
docker kill v1_http_to_mqtt_1
docker kill mysql
COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d
docker-compose run django python3 manage.py makemigrations
docker-compose run django python3 manage.py migrate


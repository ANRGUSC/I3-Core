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

# Check for prerquisites
# 1. Google API key 

if grep -Fq "<INSERT GOOGLE MAP API>" ../frontend/src/templates/products/product_map.html
then
	echo "### ERROR ###"
	echo "Warning: Please update the Google Maps API key in location :"
	echo "../frontend/src/templates/products/product_map.html"
	exit -1
else
	echo "Using admin set Goolge Maps API key"
fi

echo "Finding your IP..."
FIND_STR="DO_NOT_REMOVE"
REPLACE_STR=`curl http://checkip.amazonaws.com/`
SETTING_LCTN='../frontend/src/digitalmarket/settings.py'
CHECK=`grep $REPLACE_STR $SETTING_LCTN`

if [ -z $CHECK ]; then
        echo "IP not found in Django ALLOWED HOST"
        echo "Adding to Allowed Host at Django Setting : frontend/src/digitalmarket/settings.py"
        echo $REPLACE_STR
        echo $FIND_STR
        sed -i "s/$FIND_STR/$REPLACE_STR/" $SETTING_LCTN
fi

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


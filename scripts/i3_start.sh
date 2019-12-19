#!/bin/bash

cd ../
base="${PWD##*/*/}"
cd scripts
echo $base

LOCATION=`pwd | grep 'iotm/scripts'`

if [ -z $LOCATION ] ; then
        echo "ERROR : EXECUTION FAILED"
        echo "Please execute the script inside the scripts folder"
        exit 0
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
docker kill "$base"_parser_agent_1
docker kill "$base"_mosquitto_1
docker kill "$base"_django_1
docker kill "$base"_http_to_mqtt_1
docker kill mysql
COMPOSE_HTTP_TIMEOUT=200 docker-compose up -d
docker-compose run django python manage.py makemigrations
docker-compose run django python manage.py migrate

echo "Please enter the db password when prompted"

docker exec -it mysql mysql_config_editor set --login-path=iotm --user=default_user -p
docker exec mysql /bin/bash -c 'mysql --login-path=iotm < /var/log/mosquitto/mysql.sql'


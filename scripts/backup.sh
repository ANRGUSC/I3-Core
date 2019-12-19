#!/bin/bash

#### 
#
# Change the backup location as required. Variable named - BACKUP_LOCATION
# The backup for static files and mosquitto log is directlt inside BACKUP_LOCATION. So this would get daily updated.
# Since log and static files wouldn't get corrupted we retain this idea of having only a single copy of the data.
# For all other, the backup creation would create a foler inside the backup folder for that day.
#
####

BACKUP_LOCATION="/home/ubuntu/backup" #PLEASE NOTE NOT TO PUT / AT END
DATE=`date +%Y-%m-%d`
BACKUP=$BACKUP_LOCATION"/"$DATE

### Fetching the docker ids required ###
SQLID=`sudo docker ps -aqf "name=mysql"`
DJANGOID=`sudo docker ps -aqf "name=iotm_django_1"`

### The file names of the logs ###
SQL_FILE=$BACKUP"/"$DATE"_mysql.sql"
SERV_FILE=$BACKUP"/"$DATE"_django.json"
STATIC_FLD=$BACKUP_LOCATION"/static"
LOG_FILE=$BACKUP_LOCATION"/_mosquitto.log"

########################### MOSQUITTO LOG ####################

if [ ! -d $BACKUP_LOCATION ]; then
    mkdir $BACKUP_LOCATION
fi

mkdir $BACKUP
echo "Creating the backup folder "$BACKUP

sudo docker cp $SQLID:/var/log/mosquitto/mosquitto.log $LOG_FILE

if [ ! -f $LOG_FILE ]; then
    echo "$0: File not copied, Log not found"
fi

echo "Log file copied"
sudo chmod 666 $LOG_FILE
ls -l $LOG_FILE

########################### SQL DUMP ######################

sudo docker exec $SQLID /usr/bin/mysqldump -u default_user --password=default --databases i3database > $SQL_FILE

if [ ! -f $SQL_FILE ]; then
    echo "$0: sql dump not created."
fi

echo "SQL database dump"
sudo chmod 666 $SQL_FILE
ls -l $SQL_FILE

########################## STATIC IMAGE COPY ###############

if [ ! -d $STATIC_FLD ]; then
    mkdir $STATIC_FLD
fi

sudo docker cp $DJANGOID:/code/frontend/static_cdn/protected/ $STATIC_FLD
sudo docker cp $DJANGOID:/code/frontend/static_cdn/media/ $STATIC_FLD
sudo chmod -R 755 $STATIC_FLD
ls -l $STATIC_FLD
######################## DJANGO SERVER DUMPDATA ############

sudo docker exec $DJANGOID /code/frontend/src/manage.py dumpdata > $SERV_FILE

if [ ! -f $SERV_FILE ]; then
    echo "$0: Django dump not created."
fi

sudo chmod 666 $SERV_FILE
echo "Django server dump"
ls -l $SERV_FILE


echo "Like a Boss"

#!/bin/bash

IOTM_FOLDER=/usr/local/iotm

touch $IOTM_FOLDER/backend/log/mosquitto.log

$IOTM_FOLDER/backend/mosquitto/src/mosquitto -c $IOTM_FOLDER/backend/mosquitto/mosquitto.conf 2>&1 | tee $IOTM_FOLDER/backend/log/mosquitto.log

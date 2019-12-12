#!/bin/sh

IOTM_FOLDER=/usr/local/iotm

$IOTM_FOLDER/scripts/startup_mosquitto.sh &
$IOTM_FOLDER/scripts/startup_marketplace.sh &
$IOTM_FOLDER/scripts/startup_parser_agent.sh &
$IOTM_FOLDER/scripts/startup_publish_to_neptune.sh &

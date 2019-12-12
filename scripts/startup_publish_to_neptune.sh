#!/bin/bash

IOTM_FOLDER=/usr/local/iotm

cd $IOTM_FOLDER/gateways/bacnet
/usr/bin/python publish_to_neptune.py

#!/bin/bash

IOTM_FOLDER=/usr/local/iotm

touch $IOTM_FOLDER/frontend/log/marketplace.log

python $IOTM_FOLDER/frontend/src/manage.py runserver 0.0.0.0:8088 2>&1 | tee $IOTM_FOLDER/frontend/log/marketplace.log

#!/bin/bash

IOTM_FOLDER=/usr/local/iotm

touch $IOTM_FOLDER/backend/log/parser.log

python $IOTM_FOLDER/backend/parser_agent.py 2>&1 | tee $IOTM_FOLDER/backend/log/parser.log

# IoT Marketplace Backend

This is the back-end of the IoT Marketplace: MQTT broker, Authorization, Flow Control and Metering.

## [mosquitto-auth-plug](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/mosquitto-auth-plug)
This is a plugin to authenticate and authorize Mosquitto users.

## [parser_agent.py](https://github.com/ANRGUSC/iotm/blob/tree/crew_branch/parser_agent.py)
parse_agent.py is a real-time parser to parse the mosquitto broker log for flow control and metering.

## [parser_agent](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/parser_agent)
Folder for dockerizing the parser_agent

## [mqtt](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/mqtt)
Folder for dockerizing the backend mosquitto and mosquitto_auth_plug. `mosquitto` and `mosquitto_auth_plug` folders are no longer used.


# IoT Marketplace Backend

This is the back-end of the IoT Marketplace: MQTT broker, Authorization, Flow Control and Metering.

## [mosquitto-auth-plug](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/mosquitto-auth-plug)
This is a plugin to authenticate and authorize Mosquitto users.

## [mosquitto](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/mosquitto)
The Mosquitto broker is an open source implementation of a server for version 3.1 and 3.1.1 of the MQTT protocol. This platform serves as the pipeline between clients publishing and subscribing to I3.

## [parser_agent.py](https://github.com/ANRGUSC/iotm/blob/tree/crew_branch/parser_agent.py)
parse_agent.py is a real-time parser to parse the mosquitto broker log for flow control and metering.

## [parser_agent](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/parser_agent)
Folder for dockerizing the parser_agent

## [mqtt](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/mqtt)
Folder for dockerizing the backend mosquitto and mosquitto_auth_plug. `mosquitto` and `mosquitto_auth_plug` folders are no longer used.

## [http_to_mqtt](https://github.com/ANRGUSC/iotm/tree/crew_branch/backend/http_to_mqtt)
HTTP to MQTT client that allows HTTP requests to be translated to MQTT requests.



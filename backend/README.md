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

## Prerequisites

### Install and start mysql
```sh
$ sudo apt-get update 
$ sudo apt-get install mysql-server
$ /usr/bin/mysql_secure_installation
$ sudo service mysql start
```
### Install openssl 
```sh
$ sudo apt-get install openssl libssl-dev
```
Note: different versions of openssl may require to edit the auth plugin codes accordingly.

### Install Mosquitto MQTT Broker with Auth Plugin
Please follow the article [How to make Access Control Lists (ACL) work for Mosquitto MQTT Broker with Auth Plugin?](http://my-classes.com/2015/02/05/acl-mosquitto-mqtt-broker-auth-plugin/)
Note: edit mosquitto.conf as needed. For example, add the following information in to the configuration file:

    log_type all
    log_dest stdout
    auth_plugin /home/shangxing/mosquitto-1.4.10/auth-plug.so
    auth_opt_backends mysql
    auth_opt_host localhost
    auth_opt_port 3306
    auth_opt_dbname test
    auth_opt_user root
    auth_opt_pass 123

**Alternatively you can use the mosquitto code that you find under directory ''mosquitto'' on this github repo, which has Mosquitto 1.4.10 with Auth Plugin integrated**

If you use the mosquitto code from this Github repository, go to mosquitto/src folder and execute

```sh
$ make; make install
```

## Codes
- test_broker.py: the broker checks new pub/sub requests and manages ACL
- parse_agent.py: flow control + metering
- test_pub: the publisher
- test_sub.py: the suscriber

## Usage:
1. Start mysql server (username is 'root', password is 123):
```sh
$ mysql -u root -p
```
2. If you have not created a database, create one named *iotm*
```sh
mysql> CREATE DATABASE iotm;
```
3. Load the example user and acl tables in the database (databse: iotm):
```sh
mysql> use iotm;
mysql> source /mosquitto-auth-plug/examples/mysql.sql;
```
4. Start mosquitto broker and redirect output to test.log:
```sh
$ mosquitto -c mosquitto.conf | tee /test.log
```
License
----

MIT


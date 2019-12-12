#!/bin/sh
set -e

chown mosquitto:mosquitto -R /var/lib/mosquitto
chown mosquitto:mosquitto -R /var/log/mosquitto


if [ "$1" = 'mosquitto' ]; then
        exec /usr/local/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
fi

if [ "$1" = 'mosquittoverbose' ]; then
        exec /usr/local/sbin/mosquitto -v -c /etc/mosquitto/mosquitto.conf
fi

exec "$@"

#mosquitto -c /etc/mosquitto/mosquitto.conf

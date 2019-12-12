# Start

Run the ``i3_start.sh`` script in order to start the whole iotm project.

---

The .sh files are shell scripts that can be executed to start the processes (you can call it in /etc/rc.local). This is not a safe method, since it does not restart the processes after a crash, just starts them once.

The .service files are systemd files that can to use to start Ubuntu services during bootup time. These files have to be copied (or linked) to /etc/systemd/system. The systemd was introduced in Ubuntu 16.04, so old versions have to use upstart system
To enable the services:
$ systemctl enable <service_name>
$ systemctl start <service_name>

The files without extension are scripts to be used by System V. They have to be used on Ubuntu 14.04 or older.
To enable the services:
$ service <service_name> enable

There are three main services or scripts that need to be started:
- i3_marketplace
- i3_mosquitto
- i3_parser_agent

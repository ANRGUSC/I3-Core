#!/bin/bash

####
#
# This is to create TLS certificate using the CA cert already created.
# The CA is a self certified CA.
# We create a certificate request .csr. When filling out the form the common name is important and is usually the domain name of the server.
# You could use the IP address or Full domain name. You must use the same name when configuring the client connection.
#
# The following questions needs to be answered :

# Country Name (2 letter code) [AU]: <COUNTRY Eg. US>
# State or Province Name (full name) [Some-State]:
# Locality Name (eg, city) []:
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:
# Organizational Unit Name (eg, section) []:
# Common Name (e.g. server FQDN or YOUR name)  []: <IMPORTANT PUT THE IP/DOMAIN and the same to be used when connecting>
# Email Address []:gsramach@usc.edu
# Please enter the following 'extra' attributes
# to be sent with your certificate request
# A challenge password []:
# An optional company name []:
#####

### Server Certificate Creation ###

openssl req -new -out server.csr -key server.key

### CA key to verify and sign the server certificate. This creates the server.crt file ###

openssl x509 -req -in server.csr -CA ca.crt  -CAkey ca.key -CAcreateserial -out server.crt -days 360

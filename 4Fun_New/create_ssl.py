#!/usr/bin/python3
import os
os.system('mkdir ssl && openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365 -subj "/C=US/ST=New York/L=New York/O=General Org/OU=Ou/CN=example.com"')

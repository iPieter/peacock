#!/bin/sh

rm -rf ./build

pipenv run python main.py . -v -c --base ""

scp -r ./build/ root@pieter.ai://tmp/

ssh root@pieter.ai rm -rf /var/www/pieterai/html
ssh root@pieter.ai mv /tmp/build /var/www/pieterai/html

#ssh pieterd@ssh.cs.kuleuven.be chmod +r /cw/w3people/pieter.delobelle/public_html/resources/DBRD_gender_test_v1.zip
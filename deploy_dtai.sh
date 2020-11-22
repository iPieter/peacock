#!/bin/sh

rm -rf ./build

pipenv run python main.py . -v -c --base "/~pieter.delobelle"

scp -r ./build/ pieterd@ssh.cs.kuleuven.be:/cw/w3people/pieter.delobelle/

ssh pieterd@ssh.cs.kuleuven.be rm -rf /cw/w3people/pieter.delobelle/public_html
ssh pieterd@ssh.cs.kuleuven.be mv /cw/w3people/pieter.delobelle/build /cw/w3people/pieter.delobelle/public_html

ssh pieterd@ssh.cs.kuleuven.be chmod +r /cw/w3people/pieter.delobelle/public_html/resources/DBRD_gender_test_v1.zip
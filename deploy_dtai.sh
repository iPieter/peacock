#!/bin/sh

rm -rf ./build

pipenv run python main.py . -v -c --base "/~pieter.delobelle"

scp -r ./build/ pieterd@ssh.cs.kuleuven.be:/cw/w3people/pieter.delobelle/

ssh pieterd@ssh.cs.kuleuven.be mv /cw/w3people/pieter.delobelle/build /cw/w3people/pieter.delobelle/public_html

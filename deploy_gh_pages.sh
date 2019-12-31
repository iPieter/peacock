#!/bin/sh

rm -rf ./build
git clone git@github.com:iPieter/blog.git ./build/

rm -rf ./build/*

pipenv run python main.py . -v --base "/blog"

cd ./build
git add --all
git commit -m "Updated blog"
git push


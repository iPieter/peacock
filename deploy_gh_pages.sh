#!/bin/sh

rm -rf ../blog/build
git clone git@github.com:iPieter/blog.git ../blog/build/

rm -rf ../blog/build/*

pipenv run python main.py ../blog -v --base "/blog"

cd ../blog/build
git add --all
git commit -m "Updated blog"
git push


#!/bin/sh

svn export --username=****** --password="********" https://dcl.bas.bg/svn/marcell/Dockerfile Dockerfile

docker build --build-arg SVN_USERNAME=******** --build-arg SVN_PASSWORD="*******"  -t marcell-bg .

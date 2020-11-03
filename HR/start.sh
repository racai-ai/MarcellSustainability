#!/bin/sh

docker run --name "marcell-hr-running" -d -p 8008:8080 marcell-hr

docker ps


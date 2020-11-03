#!/bin/sh

docker run --name "marcell-sl-running" -d -p 8005:80 \
    marcell-sl

docker ps


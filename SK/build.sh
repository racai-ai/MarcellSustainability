#!/bin/sh

docker build --tag marcell-sk .


docker rmi -f $(docker images -q --filter label=builder)

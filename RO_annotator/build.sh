#!/bin/sh

docker build --tag marcell-ro .


docker rmi -f $(docker images -q --filter label=stage=intermediate)

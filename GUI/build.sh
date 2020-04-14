#!/bin/sh

docker build --tag marcell-gui .


docker rmi -f $(docker images -q --filter label=stage=intermediate)

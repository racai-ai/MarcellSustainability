#!/bin/sh

docker build --tag marcell-ro-ner .


docker rmi -f $(docker images -q --filter label=stage=intermediate)

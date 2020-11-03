#!/bin/sh

# https://github.com/zzl-ffzg/hr-marcell-pipeline.git
# git lfs pull

docker build --tag marcell-hr .

docker image prune

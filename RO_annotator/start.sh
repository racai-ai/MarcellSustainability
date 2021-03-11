#!/bin/sh

docker run --name "marcell-ro-running" -d -p 8002:80 \
    -v /data/tmp/MarcellSustainability/corpora:/corpora \
    marcell-ro

docker ps


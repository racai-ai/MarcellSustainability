#!/bin/sh

mkdir -p /data/tmp/MarcellSustainability/{corpora,runnerq,logs}
mkdir -p /data/tmp/MarcellSustainability/logs/apache2

docker run --name "marcell" -d -p=8001:80 \
    -v /data/tmp/MarcellSustainability/corpora:/site/DB/corpora \
    -v /data/tmp/MarcellSustainability/runnerq:/site/scripts/runnerq \
    -v /data/tmp/MarcellSustainability/logs:/var/log \
    marcell-gui

docker ps


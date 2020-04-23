#!/bin/sh

cron &

/ner/fastText-0.1.0-mod/fasttext server /ner/corola.300.20.5.bin 8001 &

/ner/ner_server.sh &

cd /ner/IATE-EUROVOC-Annotator/ ; ./annotate server 9001 &

/usr/sbin/apachectl -D FOREGROUND

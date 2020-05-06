#!/bin/bash

/ner/fastText-0.1.0-mod/fasttext server /ner/corola.300.20.5.bin 8001 &
/ner/ner_server.sh &

sleep 60s

export PERL5VER=`perl -V:version | grep -Po "5\.[0-9]+(?:\.[0-9]+)?"`
export PERL5LIB=/root/perl/lib/x86_64-linux-gnu/perl/$PERL5VER:/root/perl/share/perl/$PERL5VER

cd /root/nlpipe
pytest -s -v tests

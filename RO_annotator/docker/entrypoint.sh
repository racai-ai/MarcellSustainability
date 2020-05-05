#!/bin/sh

cron &

/ner/fastText-0.1.0-mod/fasttext server /ner/corola.300.20.5.bin 8001 &

/ner/ner_server.sh &

cd /ner/IATE-EUROVOC-Annotator/ ; ./annotate server 9001 &

# NLPipe tests and server start commands
export PERL5VER=`perl -V:version | grep -Po "5\.[0-9]+(?:\.[0-9]+)?"`
export PERL5LIB=/root/perl/lib/x86_64-linux-gnu/perl/$PERL5VER:/root/perl/share/perl/$PERL5VER

cd /root/nlpipe
pytest -s -v tests

if [ $? -ne 0 ]; then
	exit 1
else
	./start.ws
fi
# End NLPipe commands

/usr/sbin/apachectl -D FOREGROUND

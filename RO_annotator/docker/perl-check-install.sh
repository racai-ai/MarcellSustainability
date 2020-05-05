#!/bin/bash

# If perl version changes... No problem, we have PERL5VER now.
PERL5VER=`perl -V:version | grep -Po "5\.[0-9]+(?:\.[0-9]+)?"`
echo "perl-check-install: we got perl version = $PERL5VER"

# Set additional search directories for @INC
PERL5LIB=/root/perl/lib/x86_64-linux-gnu/perl/$PERL5VER:/root/perl/share/perl/$PERL5VER
echo "perl-check-install: added perl libraries = $PERL5LIB"

# Check perl installation
cd /root/nlpipe
perl -c PipTTL.pl

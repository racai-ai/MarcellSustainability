#!/bin/bash

# If perl version changes... No problem, we have PERL5VER now.
export PERL5VER=`perl -V:version | grep -Po "5\.[0-9]+(?:\.[0-9]+)?"`
# Set additional search directories for @INC
export PERL5LIB=/root/perl/lib/x86_64-linux-gnu/perl/$PERL5VER:/root/perl/share/perl/$PERL5VER
echo "PERL5LIB contains:"
echo -n "  "
perl -e 'print(join("\n  ", @INC) . "\n")'
# Check perl installation
cd /root/nlpipe
perl -c PipTTL.pl

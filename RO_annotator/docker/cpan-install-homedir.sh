#!/bin/bash

export PERL5VER=`perl -V:version | grep -Po "5\.[0-9]+(?:\.[0-9]+)?"`
export PERL5LIB=/root/perl/lib/x86_64-linux-gnu/perl/$PERL5VER:/root/perl/share/perl/$PERL5VER
echo "PERL5LIB contains:"
echo -n "  "
perl -e 'print(join("\n  ", @INC) . "\n")'
cpan -i File::HomeDir

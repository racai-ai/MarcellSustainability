# This the TTL NLP app for the NLPipe platform.
# TTL and all included Perl modules are (C) Radu Ion (radu@racai.ro) and ICIA 2005-2020.
use strict;
use warnings;
use utf8;
use File::HomeDir;
use IO::Socket;
use IO::Handle;
use Cwd;
use lib 'ttl/perlpak';
use pdk::ttl;
use pdk::enccnv;

sub loadROResources();
sub ttlText( $ );
sub genRandomFileName();

if ( scalar( @ARGV ) != 1 ) {
	die( "PipTTL.pl <TCP port>\n" );
}
elsif ( $ARGV[0] !~ /^[0-9]+$/ || $ARGV[0] >= 65536 ) {
	die( "PipTTL.pl <TCP port>\n" );
}

########## Config section #####################################
# Resource location, home dir/.nlpipe
my $homeDir = File::HomeDir->my_home();
my $nlpipeDir = $homeDir . "/.nlpipe";
my $sgmltwouniqFile = $nlpipeDir . "/res/sgml2unic.ent";
my $ttlResourceDir = $nlpipeDir . "/res/ro";
my $lettersAndDigits = ( "0123456789qwertyuioplkjhgfdsazxcvbnm" );
my $serverPort = shift( @ARGV );
# Tell server to exit.
my $exitCommand = "#EXIT#";
# Tell server to process text.
my $endOfTransmissionCommand = "#EOT#";
my $DEBUG = 1;
# Windows fork() does not work well; do not fork on MSWin32.
# Do not do fork when running on a dedicated uWSGI server with 1 process.
my $DONOTFORK = 1;
########## End config section ##################################

STDERR->autoflush( 1 );

if ( $DEBUG ) {
	open( DBG, ">", "ttl-debug-$serverPort.txt" ) or die( "PipTTL::main: cannot open debug file!\n" );
	DBG->autoflush( 1 );
}

print( STDERR "PipTTL::main: running on " . $^O . "\n" );

if ( $^O eq "MSWin32" ) {
	$DONOTFORK = 1;
}
else {
	# Do not accumulate zombie processes
	$SIG{"CHLD"} = "IGNORE";
}

print( STDERR "PipTTL::main: working directory is " . cwd() . "\n" );

print( STDERR "PipTTL::main: loading Unicode entities...\n" );
my( $convo ) = pdk::enccnv->new( $sgmltwouniqFile );
my( $ttlo ) = pdk::ttl->new();

# Loading resources as we start...
print( STDERR "PipTTL::main: loading Romanian TTL resources...\n" );
loadROResources();
print( STDERR "PipTTL::main: done loading.\n" );

print( STDERR "PipTTL::main: starting TCP server on port $serverPort...\n" );
# Starting a TCP/IP server on localhost.
my $ttlServer = IO::Socket::INET->new(
	'LocalHost' => "localhost",
	'LocalPort' => $serverPort,
	'Type' => SOCK_STREAM,
	'Proto' => 'tcp',
	'Reuse' => 1,
	# or SOMAXCONN
	'Listen' => 100
) or die( "PipTTL::main: can't be a TCP server on port $serverPort : $!\n" );
print( STDERR "PipTTL::main: server started.\n" );

my $clientCount = 0;

print( DBG "PipTTL::main[$clientCount]: waiting for connections on port $serverPort...\n" )
	if ( $DEBUG );

while ( my $pipClient = $ttlServer->accept() ) {
	# $pipClient is the new connection
	print( DBG "PipTTL::main[$clientCount]: connected.\n" )
		if ( $DEBUG );
		
	my $request = "";
	my $line = <$pipClient>;
	
	while ( defined( $line ) && $line !~ /^$endOfTransmissionCommand/ ) {
		$request .= $line;
		
		if ( $line =~ /^$exitCommand/ ) {
			last;
		}
		
		$line = <$pipClient>;
	}
	
	$request =~ s/^\s+//;
	$request =~ s/\s+$//;

	if ( $request eq "" ) {
		close( $pipClient );
		$clientCount++;
		
		if ( $DEBUG ) {
			print( DBG "PipTTL::main[$clientCount]: received empty request. Ignoring it.\n" );
			print( DBG "PipTTL::main[$clientCount]: waiting for connections on port $serverPort...\n" );
		}
		
		next;
	}
	
	if ( $DEBUG ) {
		print( DBG "PipTTL::main[$clientCount]: received:\n" );
		print( DBG $request . "\n" );
	}
	
	if ( $request eq $exitCommand ) {
		close( $pipClient );
		print( STDERR "PipTTL::main[$clientCount]: received $exitCommand. Bye.\n" );
		last;
	}

	if ( ! $DONOTFORK ) {
		my $pid = fork();
		
		# It may happen that the fork fails.
		# Execute the text annotation in the master.
		if ( ! defined( $pid ) || $pid == 0 ) {
			# Make text analysis multi-process so
			# that multiple clients can access the TTL
			# process.
			my $procText = ttlText( $request );

			if ( $DEBUG ) {
				print( DBG "PipTTL::main[$clientCount]: about to send back:\n" );
				print( DBG $procText . "\n" );
			}

			print( $pipClient $procText );
			close( $pipClient );
			
			if ( defined( $pid ) && $pid == 0 ) {
				# Terminate child process here.
				exit( 0 );
			}
			else {
				print( DBG "PipTTL::main: fork failed so was the master process.\n" );
			}
		}
	}
	else {
		# Single-process testing.
		my $procText = ttlText( $request );

		if ( $DEBUG ) {
			print( DBG "PipTTL::main[$clientCount]: about to send back:\n" );
			print( DBG $procText . "\n" );
		}

		print( $pipClient $procText );
		close( $pipClient );
	}
	
	$clientCount++;
	
	print( DBG "PipTTL::main[$clientCount]: waiting for connections on port $serverPort...\n" )
		if ( $DEBUG );
} # end server loop

close( DBG ) if ( $DEBUG );
######### End main.

sub ttlText( $ ) {
	my $text = $_[0];
	my $sgmltext = $convo->convert( "UTF8", "SGML", $text );
	my $ttlFile = genRandomFileName();
	my @taggedtext = ();
	
	# 1. Write text to randomly generated tmp file.
	open( SGML, ">", $ttlFile ) or die( "PipTTL::ttlText: cannot open file $ttlFile!\n" );
	binmode( SGML, ":utf8" );
	print( SGML $sgmltext . "\n" );
	close( SGML );
	
	# 2. Do TTL's sentence splitting
	my( %sent ) = %{ $ttlo->sentsplitter( $ttlFile ) };

	foreach my $p ( sort { $a <=> $b } keys( %sent ) ) {
		foreach my $s ( sort { $a <=> $b } keys( %{ $sent{$p} } ) ) {
			my( $toksent, $toktags, $nertags ) = $ttlo->tokenizer( $sent{$p}->{$s} );
			my( $tagsent, $msdsent ) = $ttlo->tagger( $toksent, $toktags, $nertags );
			my( $lemsent ) = $ttlo->lemmatizer( $toksent, $msdsent, $nertags );
			my( $chksent ) = $ttlo->chunker( $tagsent );
			my( @sent ) = ();
			
			for ( my $i = 0; $i < scalar( @{ $toksent } ); $i++ ) {
				my( $wordform ) = $toksent->[$i];
				my( $lemma ) = $lemsent->[$i];
				my( $msd ) = $msdsent->[$i];
				my( $ctag ) = $tagsent->[$i];
				my $chk = $chksent->[$i];
				
				if ( ! defined( $chk ) || $chk eq "" ) {
					$chk = "_";
				}
				
				my( $anntoken ) = $wordform . "\t" . $ctag . "\t" . $msd . "\t" . $lemma . "\t" . $chk;
				
				push( @sent, $convo->convert( "SGML", "UTF8", $anntoken ) );
			}
			
			push( @taggedtext, join( "\n", @sent ) . "\n" );
		} #end all sentences
	} #end all paragraphs
	
	unlink( $ttlFile ) or warn( "PipTTL::ttlText: could not delete file $ttlFile!" );
	return join( "\n", @taggedtext );
}

sub genRandomFileName() {
	my $fileName = "";
	
	while ( length( $fileName ) < 32 ) {
		my $randChar = substr( $lettersAndDigits, int( rand( length( $lettersAndDigits ) ) ), 1 );
		
		if ( length( $fileName ) % 2 == 0 ) {
			$fileName .= $randChar;
		}
		else {
			# Not much on Windows, but it's OK on Linux.
			$fileName .= uc( $randChar );
		}
	}
	
	return $fileName . ".tmp";
}

sub loadROResources() {
	print( STDERR "PipTTL::loadROResources: configuring Romanian sentence splitter...\n" );
	$ttlo->confsentsplitter( {
		"NERENG" => 1,
		"NERANN" => 1,
		"NERGRMM" => "$ttlResourceDir/ner_ro.rxg",
		"NERFILT" => "$ttlResourceDir/ner_ro.flt",
		"ABBREV" => "$ttlResourceDir/abbrev.ro",
		"EOLSENTBREAK" => 1,
		"NOSPLIT" => 0,
		"DEBUG" => 0
	} );

	print( STDERR "PipTTL::loadROResources: configuring Romanian tokenizer...\n" );
	$ttlo->conftokenizer( {
		"NOTOK" => 0,
		"OPORDER" => [ "split", "merge" ],
		"MERGE" => "$ttlResourceDir/merge.ro",
		"SPLIT" => "$ttlResourceDir/split.ro",
		"ENABLENAMEHEUR" => 1,
		"NAMETAG" => "NP",
		"DEBUG" => 0
	} );

	print( STDERR "PipTTL::loadROResources: configuring Romanian HMM POS tagger...\n" );
	$ttlo->conftagger( {
		"LEX" => "$ttlResourceDir/tagmod.ro.lex",
		"123" => "$ttlResourceDir/tagmod.ro.123",
		"AFX" => "$ttlResourceDir/tagmod.ro.afx",
		"SUFFL" => 5,
		"RECOVER" => 1,
		"RECOVERNER" => 0,
		"RRULES" => "$ttlResourceDir/recoverrules.ro",
		"TBLMSD" => "$ttlResourceDir/rec_tbl.ro.msd",
		"MSDSUFF" => "$ttlResourceDir/rec_suff.ro.msd",
		"MSDFREQ" => "$ttlResourceDir/rec_freq.ro.msd",
		"MSDSFXLEN" => 5,
		"TAGTOMSD" => "$ttlResourceDir/msdtag.ro.map",
		"MSDMATCH" => "^Nc|^Vm|^A",
		"MSDMAP" => { "R" => "Rgp", "Y" => "Yn", "NP" => "Np", "M" => "Mc-p-d", "S" => "Sp" },
		"DEBUG" => 0
	} );

	print( STDERR "PipTTL::loadROResources: configuring Romanian MM lemmatizer...\n" );
	$ttlo->conflemmatizer( {
		"TBL" => "$ttlResourceDir/tbl.wordform.ro.v85",
		"AMBTBL" => "$ttlResourceDir/tbl.wordform.ro.amb",
		"TAGTOMSD" => "$ttlResourceDir/msdtag.ro.map",
		"MSDTOTAG" => "$ttlResourceDir/msdtag.ro.map",
		"RECOVERED" => 1,
		"LMODEL" => "$ttlResourceDir/lemmod.ro.lm",
		"UPCASETAGS" => [ "NP", "Y" ],
		"COPYWORDFORM" => [ "Y", "M", "X" ],
		"OUTPUTTHR" => 1,
		"OUTPUTPROB" => 1,
		"DEBUG" => 0
	} );
	
	print( STDERR "PipTTL::loadROResources: configuring Romanian regex chunker...\n" );
	$ttlo->confchunker( {
		"CHUNKS" => [ "Pp", "Np", "Vp", "Ap" ],
		"GRAMFILE" => "$ttlResourceDir/rogrm.rxg",
		"MAXLINELEN" => 100
	} );
	
	print( STDERR "PipTTL::loadROResources: done configuring.\n" );
}

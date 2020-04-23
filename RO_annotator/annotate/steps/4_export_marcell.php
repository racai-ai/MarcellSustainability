<?php

function runExportMarcell($java,$fpathIn){
    global $runnerFolder,$corpus,$settings,$taskDesc;
    
    
    @chdir("corrector");
    
    passthru("$java -cp MarcellCorrection.jar Corrector ".escapeshellarg($fpathIn."/text"));

    $ret="";
    $docid="";
    foreach(glob("$fpathIn/text/*.conllup") as $fname){
	$docid=$fname;
	$ret=file_get_contents($fname);
	break;
    }
    
    @chdir("..");
    return $ret;
}

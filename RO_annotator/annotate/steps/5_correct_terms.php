<?php

function runCorrectTerms($python,$fpathIn,$fpathOut){
    global $runnerFolder,$corpus,$settings,$taskDesc;
    
    
    @chdir("corrector");
    
    passthru("$python marcell_pipe_v3.py ".escapeshellarg($fpathIn)." ".escapeshellarg($fpathOut));
    $ann=file_get_contents($fpathOut);

    @chdir("..");

    return $ann;
}

<?php

function runMarcell_sk($text,$meta,$fnameOut,$foutPath){
    global $runnerFolder,$corpus,$settings,$trun,$taskDesc,$DirectoryAnnotated;
    
    $data=MARCELL_call(
	$settings->get("marcell.sk.url","http://127.0.0.1/annotate"),
	["text"=>$text, "meta"=>$meta],
	true
    );
    
    file_put_contents($foutPath,$data);

}

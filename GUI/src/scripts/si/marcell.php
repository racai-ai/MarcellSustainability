<?php

function runMarcell_si($text,$meta,$fnameOut,$foutPath){
    global $runnerFolder,$corpus,$settings,$trun,$taskDesc,$DirectoryAnnotated;
    
    $docid=substr($fnameOut,0,strrpos($fnameOut,"."));
    
    $data=MARCELL_call(
	$settings->get("marcell.si.url","http://127.0.0.1/annotate"),
	["text"=>$text, "meta"=>$meta, "docid"=>$docid]
    );
    
    file_put_contents($foutPath,$data);

}

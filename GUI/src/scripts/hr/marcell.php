<?php

function runMarcell_hr($text,$meta,$fnameOut,$foutPath){
    global $runnerFolder,$corpus,$settings,$trun,$taskDesc,$DirectoryAnnotated;
    
    $docid=substr($fnameOut,0,strrpos($fnameOut,"."));
    
    $data=MARCELL_call(
	$settings->get("marcell.hr.url","http://127.0.0.1/annotate"),
	["text"=>$text, "metadata"=>$meta]
    );
    
    file_put_contents($foutPath,$data);

}

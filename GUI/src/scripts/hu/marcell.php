<?php

function runMarcell_hu($text,$meta,$fnameOut,$foutPath){
    global $runnerFolder,$corpus,$settings,$trun,$taskDesc,$DirectoryAnnotated;
    
    $docid=substr($fnameOut,0,strrpos($fnameOut,"."));
    
    $data=MARCELL_callWithFiles(
	$settings->get("marcell.hu.url","http://127.0.0.1/annotate"),
	["file"=>["content"=>$text."\n", "fname"=>$docid.".txt"]],
	true
    );
    
    file_put_contents($foutPath,$data);

}

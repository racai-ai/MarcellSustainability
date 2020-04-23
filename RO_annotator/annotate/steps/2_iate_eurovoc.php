<?php

function runIateEurovoc_internal($text){
    
    $data=IATE_EUROVOC_Annotate($text,0);
    if(strlen($data)>1000 || strlen($data)>strlen($text)){
	return $data;
    }else{
        echo "ERROR\n";
    }
    
    return false;
}

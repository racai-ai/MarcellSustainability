<?php

function runIateEurovoc_internal($text){
    
    $data=IATE_EUROVOC_Annotate($text,0);
    if(strlen($data)>1000 || strlen($data)>strlen($text)){

        // migrate EUROVOC in the last column (col 14 => col 15, col 14 = _)
        $retData="";
        foreach(explode("\n",$data) as $line){
            if(strlen($line)==0 || $line[0]=="#"){$retData.=$line."\n"; continue;}
            $ldata=explode("\t",$line);
            if(count($ldata)<14){$retData.=$line."\n"; continue;}
            $ldata[]=$ldata[13];
            $ldata[13]="_";
            $retData.=implode("\t",$ldata)."\n";
        }

	return $retData;
    }else{
        echo "ERROR\n";
    }
    
    return false;
}

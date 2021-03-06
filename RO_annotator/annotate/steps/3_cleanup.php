<?php

function cleanFileContent($fcontent,$meta){
    $retData="";
    $lines="";
    $linesOK=false;
    $numLines=0;
    $nonSym=0;
    $annOK=true;
    $firstWrite=true;
    $allowedNER=array_flip(["O","B-ORG","I-ORG","B-PER","I-PER","B-TIME","I-TIME","B-LOC","I-LOC"]);
    $numColumns=0;
    foreach(explode("\n",$fcontent."\n") as $line){
        $line=trim($line);
        if(strlen($line)===0){
            if($linesOK && $numLines>0 && $nonSym>0 && $annOK){
            	if($firstWrite){
            	    if(!startsWith($lines,"# global.columns")){
                      if($numColumns>12){
            		          $lines="# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC RELATE:NE RELATE:NP RELATE:IATE RELATE:EUROVOCID RELATE:EUROVOCMT\n".$meta.$lines;
                      }else{
            		          $lines="# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC RELATE:NE RELATE:NP\n".$meta.$lines;
                      }
            	    }
            	}
            	$retData.=$lines."\n";
            	$firstWrite=false;
	          }
            $lines="";
            $linesOK=false;
            $numLines=0;
            $nonSym=0;
            $annOK=true;
        }else{
            $lines.=$line."\n";
            if($line[0]!='#'){
                $ldata=explode("\t",$line);
                if(count($ldata)>$numColumns)$numColumns=count($ldata);
                if(count($ldata)>6 && strcasecmp($ldata[6],"0")!=0){
            	    $linesOK=true;$numLines++;
            	}
            	if(count($ldata)>3 && $ldata[3]!='SYM')$nonSym++;
                if(count($ldata)>10 && !isset($allowedNER[$ldata[10]]))$annOK=false;
                if(count($ldata)<13)$annOK=false;
            }
        }
    }
    
    return $retData;
}


?>
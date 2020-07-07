<?php

function runMarcell($text,$fout){
    global $corpus;
    
    runMarcell_internal($text,$fout);
    
    file_put_contents($corpus->getFolderPath()."/changed_basictagging.json",json_encode(["changed"=>time()]));            
}

function runMarcell_internal($text,$fout){
    echo "runMarcell_internal => $fout\n";
    
    global $runnerFolder,$corpus,$settings,$trun,$taskDesc,$DirectoryAnnotated;

    $lang=$corpus->getData("lang","en");
    echo "LANG=$lang\n";

    $meta="";
    $pos=strrpos($fout,".");
    $mfname=$fout;
    if($pos!==false){$mfname=substr($fout,0,$pos);}
    $metaPath=$corpus->getFolderPath()."/standoff/".$mfname;
    if(is_file($metaPath.".xml"))$meta=file_get_contents($metaPath.".xml");
    else if(is_file($metaPath.".meta"))$meta=file_get_contents($metaPath.".meta");
    else if(is_file($metaPath.".metadata"))$meta=file_get_contents($metaPath.".metadata");
    else echo "METADATA file not found for [$metaPath]\n";

    // For Romanian we need to determine the final filename/docid
    $docid="";
    if($lang=="ro"){
	$docid=$fout;
	$fout=substr($fout,3);
	$fout=substr($fout,0,strrpos($fout,"."));
	$xml = simplexml_load_string($meta);
	$json = json_encode($xml);
	$array = json_decode($json,TRUE);
	$year=0;
	if(isset($array['root']))$array=$array['root'];
	if(isset($array['Metadata']))$array=$array['Metadata'];
	if(isset($array['PublicationDate']))$year=$array['PublicationDate'];
	$fout="ro-mj-".$year."-".$fout.".conllup";
    }else{
	$pos=strrpos($fout,".");
	if($pos!==false)$fout=substr($fout,0,$pos);
	$fout.=".conllup";
    }
    
    $path=$corpus->getFolderPath()."/$DirectoryAnnotated/";
    $finalFile=$path.$fout;
    if(is_file($finalFile)){
        if(filesize($finalFile)>0 && isset($taskDesc['overwrite']) && $taskDesc['overwrite']===false){
            echo "SKIP $fout\n";
            return false;
        }
    
        $fmtime=filemtime($finalFile);
        $tctime=strtotime($taskDesc['created_date']);
        if($fmtime>$tctime && filesize($finalFile)>100){
            echo "SKIP $fout\n";
            return false;
        }
    }
    
    
    @mkdir($path);    
    
    if($lang=="bg"){
        runMarcell_bg($text,$meta,$fout,$finalFile);
    }else if($lang=="hr"){
        runMarcell_hr($text,$meta,$fout,$finalFile);
    }else if($lang=="hu"){
        runMarcell_hu($text,$meta,$fout,$finalFile);
    }else if($lang=="pl"){
        runMarcell_pl($text,$meta,$fout,$finalFile);
    }else if($lang=="ro"){
        runMarcell_ro($text,$meta,$docid,$finalFile);
    }else if($lang=="sk"){
        runMarcell_sk($text,$meta,$fout,$finalFile);
    }else if($lang=="si"){
        runMarcell_si($text,$meta,$fout,$finalFile);
    }else {
	echo "Unknown corpus lang [$lang]\n";
	return false;
    }
}

function MARCELL_call($url,$data,$debug=false){

    echo "MARCELL_call [$url]\n";

    if(!isset($data['text']))return false;

    $ch = curl_init();
  
    set_time_limit(0);
    ini_set("default_socket_timeout", 600);
    
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 0); 
    curl_setopt($ch, CURLOPT_TIMEOUT_MS, 600 * 1000); //timeout in seconds
    curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
    curl_setopt($ch, CURLOPT_URL,$url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Expect:'));
    if($debug)curl_setopt($ch, CURLOPT_VERBOSE, 1); 

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $server_output = curl_exec($ch);
    
    curl_close ($ch);
    
    return $server_output;

}

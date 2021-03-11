<?php

require_once "lib/lib.php";
require_once "steps/1_basic_tagging.php";
require_once "steps/2_iate_eurovoc.php";
require_once "steps/3_cleanup.php";
require_once "steps/4_eurovoc_class.php";
require_once "steps/5_correct_terms.php";
require_once "steps/6_export_marcell.php";

if(!isset($_REQUEST['text']) || !isset($_REQUEST['meta']) || !isset($_REQUEST['docid'])){
    die("Invalid usage. Required: text,meta,docid");
}

$text=$_REQUEST['text'];
$meta=$_REQUEST['meta'];
$docid=$_REQUEST['docid'];

//echo "TEXT=";var_dump($text);
//echo "META=";var_dump($meta);
//echo "DOCID=";var_dump($docid);

$ann=runBasicTaggingText_ro($text);
//echo "BASIC TAGGING=";var_dump($ann);
$ann=runIateEurovoc_internal($ann);
//echo "IATE/EUROVOC=";var_dump($ann);
$ann=cleanFileContent($ann,"");
//echo "CLEAN=";var_dump($ann);
$ann=runEurovocClass($ann);

// Write temporary files
$tmpfolder=uniqid("r",true);
$dir=dirname(__FILE__);
@mkdir("$dir/corrector/$tmpfolder");
@mkdir("$dir/corrector/$tmpfolder/text");
$fnameAnn="$tmpfolder/text/$docid.txt";
file_put_contents("$dir/corrector/$fnameAnn",$ann);
@mkdir("$dir/corrector/$tmpfolder/standoff");
file_put_contents("$dir/corrector/$tmpfolder/standoff/$docid.xml",$meta);

// Remove shorter terms
$python="/usr/bin/python3";
runCorrectTerms($python,$fnameAnn,$fnameAnn);

// Adjust the format
$java="/ner/jdk1.8.0_191/bin/java";
$ann=runExportMarcell($java,$tmpfolder);

passthru("rm -fr $dir/corrector/$tmpfolder");

echo $ann;

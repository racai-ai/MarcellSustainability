<?php

function runExportMarcell($pathIn){
    global $runnerFolder,$corpus,$settings,$taskDesc;
    
    @chdir("marcell");
    passthru("./marcell_xml_all.sh ".escapeshellarg($settings->get("tools.python.venv"))." ".escapeshellarg($corpus->getFolderPath()));
    @chdir("..");
    
    $marcellOut=$corpus->getFolderPath()."/marcell-out";
    $lang=$corpus->getData("lang","en");
    $d=date("Ymd");
    @mkdir($marcellOut);
    @unlink("$marcellOut/$lang-annotated-$d.zip");
    @unlink("$marcellOut/$lang-raw-$d.zip");
    @unlink("$marcellOut/$lang-xml-$d.zip");
    
    passthru("zip -r -j -9 ".escapeshellarg("$marcellOut/$lang-raw-$d.zip")." ".escapeshellarg($corpus->getFolderPath()."/files"));
    passthru("zip -r -j -9 ".escapeshellarg("$marcellOut/$lang-annotated-$d.zip")." ".escapeshellarg($corpus->getFolderPath()."/basic_tagging"));
    passthru("zip -r -j -9 ".escapeshellarg("$marcellOut/$lang-xml-$d.zip")." ".escapeshellarg($corpus->getFolderPath()."/marcell-xml"));
}

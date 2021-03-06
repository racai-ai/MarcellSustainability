<?php

function runEurovocClass($contentIn){
    $conllup=new \CONLLUP();
    $conllup->readFromString($contentIn);
    $data=EUROVOC_Classify($conllup->getText(),6,0.0,1); // runner id =1
    if($data!==false){
        $mtids=EUROVOC_getMT($data);
        $domains=EUROVOC_getDomains($mtids);
        sort($domains);
        $conllup->addFileMetadataField("eurovoc",implode("\t",$domains));
        return $conllup->writeToString();
    }

    echo "Error EUROVOC CLASS";

    return $contentIn;
}

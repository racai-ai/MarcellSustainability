<?php

function testNER($tokData){
    $url="http://127.0.0.1:8002/ner/ner.php";
    
    $curl = curl_init();
    
    //$url_data = http_build_query($data);
    
    $boundary = uniqid();
    $delimiter = '-------------' . $boundary;
    $eol = "\r\n";
    $data="";
    $data .= "--" . $delimiter . $eol
                . 'Content-Disposition: form-data; name="tokens"'.$eol.$eol
                . $tokData . $eol;
    $data .= "--" . $delimiter . "--".$eol;

    curl_setopt_array($curl, array(
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        //CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "POST",
        CURLOPT_POST => 1,
        CURLOPT_POSTFIELDS => $data,
        CURLOPT_HTTPHEADER => array(
          //"Authorization: Bearer $TOKEN",
          "Content-Type: multipart/form-data; boundary=" . $delimiter,
          "Content-Length: " . strlen($data)
      
        ),
    ));

    $response = curl_exec($curl);
    curl_close($curl);
    return $response;
}

$tokdata=file_get_contents("testner.test");
var_dump(testNER($tokdata));

?>
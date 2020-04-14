<?php

function getPageContent(){
    $html=file_get_contents(realpath(dirname(__FILE__))."/home.html");
    
    return $html;
}

function getPageCSS(){
}

function getPageJS(){
}

?>
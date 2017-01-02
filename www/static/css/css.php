<?php

function isBuggyIe() {
    $ua = $_SERVER['HTTP_USER_AGENT'];
    // quick escape for non-IEs
    if (0 !== strpos($ua, 'Mozilla/4.0 (compatible; MSIE ')
        || false !== strpos($ua, 'Opera')) {
        return false;
    }
    // no regex = faaast
    $version = (float)substr($ua, 30); 
    return (
        $version < 6
        || ($version == 6  && false === strpos($ua, 'SV1'))
    );
}


if(!isBuggyIe()&&extension_loaded('zlib'))ob_start('ob_gzhandler');
header("Content-type: text/css");

$files = scandir(dirname(__FILE__));
foreach($files as $file){
    if(@end($tmp=@explode('.',$file))=='css'){
        include(dirname(__FILE__).'/'.$file);
    }
}

if(!isBuggyIe()&&extension_loaded('zlib')){ob_end_flush();}

?>
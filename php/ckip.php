<?php
function ckip($text, $options=array()){
    if(!array_key_exists("encoding", $options)) $options["encoding"]="UTF-8, BIG-5";
    $encoding=mb_detect_encoding($text, $options["encoding"]);
    if(!$encoding) return array(); // Encoding detection failure.
    $curl_options=array( // Fixed curl options here.
        CURLOPT_HEADER=>0,
        CURLOPT_VERBOSE=>0,
        CURLOPT_RETURNTRANSFER=>TRUE,
        CURLOPT_USERAGENT=>"Mozilla/4.0 (compatible;)",
        CURLOPT_POST=>TRUE,
    );
    if(array_key_exists("version", $options)){
        if($encoding!=="BIG-5") $text=iconv($encoding, "BIG-5//TRANSLIT", $text);
        $curl_options[CURLOPT_URL]="http://140.116.245.145/cgi-bin/ckip/".$options["version"].".cgi";
        $curl_options[CURLOPT_POSTFIELDS]="query $text";
    }
    else{
        if($encoding!=="UTF-8") $text=mb_convert_encoding($text, "UTF-8", $encoding);
        $curl_options[CURLOPT_URL]="http://140.116.245.151/ckip.php";
        $curl_options[CURLOPT_POSTFIELDS]=array("text"=>$text);
    }
    set_time_limit(0); // 0 is infinite.
    $ch=curl_init();
    curl_setopt_array($ch, $curl_options);
    $result=curl_exec($ch);
    curl_close($ch);
    $value=array(); // The final result.
    if(array_key_exists("version", $options)) $result=mb_convert_encoding($result, "UTF-8", "BIG-5");
    $count=preg_match_all("/([^\n\x{3000}]+)\((.*?)\)/u", $result, $result_array);
    for($i=0; $i<$count; $i++){
        $value[$i]["term"]=$result_array[1][$i];
        $value[$i]["tag"]=$result_array[2][$i];
        if(array_key_exists("form", $options)) $value[$i]["term"]=normalizer_normalize($value[$i]["term"], $options["form"]);
        if($encoding!=="UTF-8") $value[$i]["term"]=mb_convert_encoding($value[$i]["term"], $encoding, "UTF-8");
    }
    return $value;
}

if(!count(debug_backtrace())){
    $USAGE="Usage: ".$argv[0]." [-e <encoding>] [-v <version>] [-f <filename>|-t <text>]".PHP_EOL;
    $opt=getopt("e:f:t:v:");
    $ckip_options=array();
    if(array_key_exists("e", $opt)) $ckip_options["encoding"]=$opt["e"];
    if(array_key_exists("v", $opt)) $ckip_options["version"]=$opt["v"];
    if(array_key_exists("t", $opt)){
        !array_key_exists("f", $opt) or die($USAGE);
        print_r(ckip($opt["t"], $ckip_options));
    }
    else if(array_key_exists("f", $opt)){
        !array_key_exists("t", $opt) or die($USAGE);
        $text=file_get_contents($opt["f"]);
        print_r(ckip($text, $ckip_options));
    }
    else die($USAGE);
}
?>

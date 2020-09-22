<?php
  $request = "https://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
  $base = basename(getcwd());
  if ($_SERVER[REQUEST_URI] == "/$base/create" or $_SERVER[REQUEST_URI] == "/$base/create/"){
    require("shortener.html");
    if ($_POST["url"]){
      $toshorten = $_POST["url"];
      $shortener = exec("python3 main.py --create $toshorten 2>&1");
      echo($shortener);
    }
  }else{

  $dest = exec("python3 main.py --request $request 2>&1");

  if ($dest == "None"){
    http_response_code(404);
    echo("404: Resource not found.");
  } else {
    echo($dest);
    header("HTTP/1.1 301 Moved Permanently");
    header("Location: $dest");
  }
  }
?>

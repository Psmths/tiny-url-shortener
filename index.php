<?php
  $request = "https://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
  $base = basename(getcwd());
  if ($_SERVER[REQUEST_URI] == "/$base/create" or $_SERVER[REQUEST_URI] == "/$base/create/"){
    require("shortener.html");
    if ($_POST["url"]){
      $shortener = exec("python3 main.py --create ".escapeshellcmd($_POST["url"])." 2>&1");
      echo($shortener);
    }
  }else{
    $dest = exec("python3 main.py --request ".escapeshellcmd($request)." 2>&1");
    if ($dest == "None"){
      http_response_code(404);
      echo("404: Resource not found.");
    } else {
      header("HTTP/1.1 301 Moved Permanently");
      header("Location: $dest");
    }
  }
?>

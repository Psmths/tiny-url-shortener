<?php
  $request = "https://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
  $base = basename(getcwd());
  if ($_SERVER[REQUEST_URI] == "/$base/create" or $_SERVER[REQUEST_URI] == "/$base/create/"){
    require("shortener.html");
    if ($_POST["url"]){
      $shortener = exec(escapeshellcmd("python3 main.py --create ".escapeshellarg($_POST["url"])));
      echo($shortener);
    }
  }else{
    $dest = exec(escapeshellcmd("python3 main.py --request ".escapeshellarg($request)));
    if ($dest == "None"){
      http_response_code(404);
      echo("404: Resource not found.");
    } else {
      header("HTTP/1.1 301 Moved Permanently");
      header("Location: $dest");
    }
  }
?>

<?php

$dir="/home/Grads/2012/bnb32/public_html/tools/";

$script=$_GET["script"];
$cmd="python " . $dir . "run.py " . $script;
if ($script == "addsong") {
    $song=$_GET["song"];
    $user=$_GET["user"];
    $level=$_GET["level"];
    $cmd=$cmd . ' "' . $song . '" ' . $user . ' ' . $level;
}
if ($script == "wrongsong") {
    $user=$_GET["user"];
    $cmd=$cmd . ' ' . $user;
}      
$command=escapeshellcmd($cmd);
$output=shell_exec($command);
print($output)

?>

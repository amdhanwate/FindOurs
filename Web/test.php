<?php

$result = exec("python C:/Abhi/XAMPP/htdocs/FindOURS/fingerprint_recognition/fingerprint-recognition/app_new.py \"101_1.tif\"", $output, $retval);

print_r($output);
echo $retval;

?>
<?php 

$json = file_get_contents("loginData.json");
$data = json_decode($json, $associative= true);

echo gettype($data);
$input_authID = $_POST["authID"];
$input_password = $_POST["authPassword"];

$length = count($data);

for ($i=0; $i<$length; $i++) {
    // echo gettype($data["$i"]["password"]);
    if ($data["$i"]["authID"] == $input_authID && $data[$i]["password"] == $input_password) {
        echo "Success";
        header("Location: home.html");
    } else {
        continue;
    }
}

?>
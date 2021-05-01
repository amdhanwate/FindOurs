<?php 

$json = file_get_contents("loginData.json");
$data = json_decode($json, $associative= true);

// echo gettype($data);
$input_authID = $_POST["authID"];
$input_password = $_POST["authPassword"];


$validUser = "";
if(isset($_POST["submit"])) {
    $validUser = $input_authID == $data["authID"] && $input_password == $data["password"];
    if(!$validUser) $errorMsg = "Invalid username or password.";
    else $_SESSION["login"] = true;
  }
  if($validUser) {
     header("Location: ./home.html"); die();
  } else {
      echo $errorMsg;
  }

?>

<?php
// $length = count($data);
// $msg=  "
//         <script>
//             alert('Wrong ID or Password!!');
//         </script>
//         ";

// if ($input_authID == $data["authID"]){
//     if ($input_password == $data["password"]){
//         header("Location: home.html");
//     }
//     else {
//         echo $msg;
//         header("Location: login.html");
//     }
// } else {
//     echo $msg;
//     header("Location: login.html");
// }

// for ($i=0; $i<$length; $i++) {
//     // echo gettype($data["$i"]["password"]);
//     if ($data["$i"]["authID"] == $input_authID && $data[$i]["password"] == $input_password) {
//         echo "Success";
//         header("Location: home.html");
//     } else {
//         continue;
//     }
// }
?>

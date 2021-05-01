<?php
if (isset($_FILES['uploadFile'])) {
   $errors = array();
   $file_name = $_FILES['uploadFile']['name'];
   $file_size = $_FILES['uploadFile']['size'];
   $file_tmp = $_FILES['uploadFile']['tmp_name'];
   $file_type = $_FILES['uploadFile']['type'];
   // $file_ext=strtolower(end(explode('.', $file_name)));s

   // echo $file_name;
   $extensions = array("jpeg", "jpg", "png");

   // if(in_array($file_ext,$extensions)=== false){
   //    $errors[]="extension not allowed, please choose a JPEG or PNG file.";
   // }

   if ($file_size > 2097152) {
      $errors[] = 'File size must be excately 2 MB';
   }

   if (empty($errors) == true) {
      move_uploaded_file($file_tmp, "uploads/" . $file_name);
      // echo "Success";
   } else {
      print_r($errors);
   }


   $result = exec("python C:/Abhi/XAMPP/htdocs/FindOURS/fingerprint_recognition/fingerprint-recognition/app_new.py \"$file_name\"", $output, $retval);
   // echo $result;

   $matchedImg = $output[0];

   $json = file_get_contents("C:/Abhi/XAMPP/htdocs/FindOURS/Web/data_new.json");
   // C:/Abhi/XAMPP/htdocs/FindOURS/fingerprint_recognition/fingerprint-recognition/data.json
   $json = json_decode($json, true);

   if ($matchedImg != "NMF") {
      $matchedPersonName = (string)$json[$matchedImg]["name"];
      $matchedPersonAge = (string)$json[$matchedImg]["age"];
      $matchedPersonGender = (string)$json[$matchedImg]["gender"];
      $matchedPersonMobile = (string)$json[$matchedImg]["mobile"];
      $matchedPersonAddress = (string)$json[$matchedImg]["address"];
      $matchedPersonImage = (string)$json[$matchedImg]["image"];
      // echo $matchedPersonImage;
      
      $html =
         '
            <!DOCTYPE html>
            <html lang="en">
            
            <head>
               <meta charset="UTF-8">
               <meta http-equiv="X-UA-Compatible" content="IE=edge">
               <meta name="viewport" content="width=device-width, initial-scale=1.0">
               <title>Success</title>
               <link rel="stylesheet" href="styles/main.css">
               <link rel="stylesheet" href="styles/connect.css">
            </head>
            
            <body>
               <nav id="navbar">
                  <img src="images/navbar96.png" alt="FindOurs Logo">
                  <p id="app-name">FIND OURS</p>
                  <p id="signout" onclick="logout()"><a><img src="images/signout.png" alt="Sign Out"></a></p>
               </nav>
               <h1 class="page-head">DETAILS OF THE PERSON</h1>
               <main>
                  <div class="img"><img class="pimg" src="%s" /></div>
                  <div class="container">
                     <div>
                           <p>Name: </p>
                           <p class="value">%s</p>
                     </div>
                     <div>
                           <p>Age: </p>
                           <p class="value">%s</p>
                     </div>
                     <div>
                           <p>Gender: </p>
                           <p class="value">%s</p>
                     </div>
                     <div>
                           <p>Mobile: </p>
                           <p class="value">%s</p>
                     </div>
                     <div>
                           <p>Address: </p>
                           <p class="value">%s</p>
                     </div>
                  </div>
               </main>
               <div class="buttons">
                  <a href="search.html" class="btn btn-blue">Search Another Person</a>
                  <a href="home.html" class="btn btn-red">Back to Home</a>
               </div>
            </body>
            
            </html>
            ';

      // echo gettype($matchedPersonAge);
      // echo gettype($matchedPersonName);
      // echo $html;
      printf($html, $matchedPersonImage, $matchedPersonName, $matchedPersonAge, $matchedPersonGender, $matchedPersonMobile, $matchedPersonAddress);
   } else {
      $html = '
      <!DOCTYPE html>
      <html lang="en">
      
      <head>
         <meta charset="UTF-8">
         <meta http-equiv="X-UA-Compatible" content="IE=edge">
         <meta name="viewport" content="width=device-width, initial-scale=1.0">
         <title>Success</title>
         <link rel="stylesheet" href="styles/main.css">
         <link rel="stylesheet" href="styles/connect.css">
      </head>
      
      <body>
         <nav id="navbar">
            <img src="images/navbar96.png" alt="FindOurs Logo">
            <p id="app-name">FIND OURS</p>
            <p id="signout" onclick="logout()"><a><img src="images/signout.png" alt="Sign Out"></a></p>
         </nav>
         <h1 class="page-head" style="color: red; position: relative; top: 30vh;">NO DATA FOUND!!</h1>
         <div class="container">
            <p></p>
         </div>
      </body>
         
      </html>
      ';
      
      printf($html);

   }
}

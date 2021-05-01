<?php
if (isset($_FILES['uploadFile'])) {
   $errors = array();

   $file_name = $_FILES['uploadFile']['name'];

   // $extensions = array("jpeg", "jpg", "png");

   // if ($file_size > 2097152) {
   //    $errors[] = 'File size must be excately 2 MB';
   // }

   if (empty($errors) == true) {
      move_uploaded_file($file_tmp, "uploads/" . $file_name);
      // echo "Success";
   } else {
      print_r($errors);
   }


   $result = exec("python C:/Abhi/XAMPP/htdocs/FindOURS/FINDOURS/fingerprint_recognition/fingerprint-recognition/app_new.py \"$file_name\"", $output, $retval);
   $matchedImg = $output[0];

   $json = file_get_contents("C:/Abhi/XAMPP/htdocs/FindOURS/FINDOURS/fingerprint_recognition/fingerprint-recognition/data.json");
   $json = json_decode($json, true);

   if (!$matchedImg = "NMF") {
      $matchedPersonName = (string)$json[$matchedImg]["name"];
      $matchedPersonAge = (string)$json[$matchedImg]["age"];
      $css =
         '
            <style>
               .container {
                  width: 50\%;
                  margin: auto;
                  position: relative;
                  top: 20vh;
                  display: flex;
                  flex-direction: column;
                  align-items: center;
                  justify-content: center;
               }
      
               span {
                  text-decoration: underline red;
               }
      
               .btn {
                  text-align: center;
                  display: flex;
                  /* justify-content: center; */
                  margin: 20px auto auto;
                  align-items: center;
                  flex-direction: column;
                  position: relative;
                  top: 40vh;
                  color: #eee;
                  width: fit-content;
                  padding: 5px 10px;
               }
      
               .btn-blue{
                  background-color: #55e;
               }
      
               .btn-red {
                  background-color: #e55;
               }
            </style>
            ';
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
               <link rel="stylesheet" href="styles/search.css">
               %s
            </head>
            
            <body>
               <nav id="navbar">
                  <img src="images/navbar96.png" alt="FindOurs Logo">
                  <p id="app-name">FIND OURS</p>
                  <p id="signout" onclick="logout()"><a><img src="images/signout.png" alt="Sign Out"></a></p>
               </nav>
               <h1 class="page-head">DETAILS OF THE PERSON</h1>
               <div class="container">
                  <p>Name: <span> %s </span></p>
                  <p>Age: <span> %s </span></p>
               </div>
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
      printf($html, $css, $matchedPersonName, $matchedPersonAge);
   } else {
      echo "No data found!";
   }
}

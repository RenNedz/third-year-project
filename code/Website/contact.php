<?php
//if the name has been correctly passed from the HTML form, it's set to the variable $name
  if(isset($_POST['name'])){	
   $name = $_POST['name'];
  }else{
    $name = "John";		//dummy name
  }
  
  
//if the email has been correctly passed from the HTML form, it's set to the variable $email
  if(isset($_POST['email'])){
    $email = $_POST['email'];
  }else{
    $email = "xyz@xyz.com";	//dummy email
  }

//if the message has been correctly passed from the HTML form, it's set to the variable $email
  if(isset($_POST['message'])){
	$msg = $_POST['message'];
  }else{
	$msg = "hello";
  }


  $receiver ='brexitanalysis@gmail.com';
  $header= "FROM: $name\n $email";
  $query="MESSAGE:\n $msg";
  
  //sends header message detailing the name and sending email to the brexit analysis email 
  mail ($receiver, $header, $query);
  
  //redirects user to a query confirmation page
  header("Location: query-received.php");

?>
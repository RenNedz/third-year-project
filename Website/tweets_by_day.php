<?php
//database details

$dbuser = 'tweet_sys';
$password = 'admin_pass';
$dbname = 'Tweets';

//establishes connection to the database
$conn = new mysqli('localhost', $dbuser, $password, $dbname);
if ($conn->connect_error) {
  trigger_error('Database connection failed: '  . $conn->connect_error, E_USER_ERROR);
}

$statement = "SELECT date, count(date) as nr_of_tweets FROM Tweet GROUP BY date";

//queries statement via the established connection
$results=$conn->query($statement);

////result will be equal to each row in the database containing a valid data until none are left
while($result = mysqli_fetch_array($results))
{
  $val = "Date(";
  $t = $result['date'];
  $val .= substr($t, 0, 4);
  $val .= ", ";
  $month = substr($t, 5, 2);
  if($month == "01")
  	$month = "00";
  else if($month == "02")
  	$month = "01";
  else if($month == "03")
  	$month = "02";
  else if($month == "04")
  	$month = "03";
  else if($month == "05")
  	$month = "04";
  else if($month == "06")
  	$month = "05";
  else if($month == "07")
  	$month = "06";
  else if($month == "08")
  	$month = "07";
  else if($month == "09")
  	$month = "08";
  else if($month == "10")
  	$month = "09";
  else if($month == "11")
  	$month = "10";
  else if($month == "12")
  	$month = "11";
  $val .= $month;
  $val .= ", ";
  $val .= substr($t, 8, 2);
  $val .= ")";
  
  //results are added to the array and initial Google Charts formatting is set
  $array[]=array("c"=>array("0"=>array("v"=>$val,"f"=>NULL),"1"=>array("v"=>(int)$result['nr_of_tweets'],"f" =>NULL)));
}

//Full JSON format as required by Google Charts API - these paramters will be passed into the chart in order to produce it on the page
echo $format = "{
	\"cols\": [
	{\"id\":\"\",\"label\":\"date\",\"pattern\":\"\",\"type\":\"date\"},
	{\"id\":\"\",\"label\":\"count\",\"pattern\":\"\",\"type\":\"number\"}
	],
	\"rows\":".json_encode($array)."}";
	
//closes connection to the database
$conn->close();

?>
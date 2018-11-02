<?php
#This script returns the sentiment of tweets regarding brexit within a country

//database details
$dbuser = 'tweet_sys';
$password = 'admin_pass';
$dbname = 'Tweets';

//establishes a connection to our MySQL database using the details above
$conn = new mysqli('localhost', $dbuser, $password, $dbname);
if ($conn->connect_error) {
  trigger_error('Database connection failed: '  . $conn->connect_error, E_USER_ERROR);
}

//Get arguments supplied by HTML form for country, search string, sentiment and stance
if(isset($_POST['country']))
{
  $country = $_POST['country'];
}
if(isset($_POST['sentiment']))
{
  $sentiment = $_POST['sentiment'];
}
if(isset($_POST['stance']))
{
  $stance = $_POST['stance'];
}
if(isset($_POST['search_string']))
{
  $search_string = $_POST['search_string'];
}

//Begin building statement
if($country == "All")
{
    //Group by Country
  $option = 1;
  $s = "";
  if($sentiment != "none")
  {
  	$s .= "AND sentiment like \"%$sentiment%\" ";
  }
  if($stance != "none")
  {
  	$s .= "AND stance like \"%$stance%\" ";
  }
  if($search_string != "")
  {
  	$s .= "AND text like \"%$search_string%\" ";
  }
  $statement = "SELECT (SELECT count(country) FROM Tweet where country like \"%england%\" $s) AS england, (SELECT COUNT(country) FROM Tweet WHERE country like \"%ireland%\" $s) as ireland, (SELECT COUNT(country) FROM Tweet WHERE country like \"%n. ireland%\" $s) as nireland, (SELECT COUNT(country) FROM Tweet WHERE country like \"%scotland%\" $s) as scotland, (SELECT COUNT(country) FROM Tweet WHERE country like \"%wales%\" $s) as wales FROM Tweet GROUP BY ireland";
}
else if($sentiment == "All")
{
    //Group by sentiment
  $option = 2;
  $s = "";
  if($country != "none")
  {
  	$s .= "AND country like \"%$country%\" ";
  }
  if($stance != "none")
  {
  	$s .= "AND stance like \"%$stance%\" ";
  }
  if($search_string != "")
  {
  	$s .= "AND text like \"%$search_string%\" ";
  }
  $statement = "SELECT (SELECT count(id) FROM Tweet where sentiment like \"%Pos%\" $s) AS pos, (SELECT count(id) FROM Tweet where sentiment like \"%Neg%\" $s) as neg, (SELECT count(id) FROM Tweet where sentiment like \"%Neu%\" $s) FROM Tweet GROUP BY pos";
}
else if($stance == "All")
{
    //Group by stance
  $option = 3;
  $s = "";
  if($country != "none")
  {
  	$s .= "AND country like \"%$country%\" ";
  }
  if($sentiment != "none")
  {
  	$s .= "AND sentiment like \"%$sentiment%\" ";
  }
  if($search_string != "")
  {
  	$s .= "AND text like \"%$search_string%\" ";
  }
  $statement = "SELECT (SELECT count(id) FROM Tweet where stance like \"%Pro_brexit%\" $s) as ex, (SELECT count(id) FROM Tweet where stance like \"%Pro_stay%\" $s) as stay FROM Tweet GROUP BY stay";
}

//a connection is made, the statement is then queried against the database and stored in the variable $results
$results=$conn->query($statement);

//if group by country has been supplied from form
if($option == 1)
{
    //result will be equal to each row in the database containing the country until none are left
	if ($result = mysqli_fetch_array($results))
	{
	    //if the results from the query are not equal to 0 for all the countries for england, ireland, n.ireland, scotland and wales
	    //then add the total from each country into a individual array slot
		if((int)$result['england'] != 0 || (int)$result['ireland'] != 0 || (int)$result['n. ireland'] != 0 || (int)$result['scotland'] != 0 || (int)$result['wales'] != 0)
		{
			$array[0]=array("c"=>array("0"=>array("v"=>"England","f"=>NULL),"1"=>array("v"=>(int)$result['england'])));
			$array[1]=array("c"=>array("0"=>array("v"=>"Ireland","f"=>NULL),"1"=>array("v"=>(int)$result['ireland'])));
			$array[2]=array("c"=>array("0"=>array("v"=>"N. Ireland","f"=>NULL),"1"=>array("v"=>(int)$result['nireland'])));
			$array[3]=array("c"=>array("0"=>array("v"=>"Wales","f"=>NULL),"1"=>array("v"=>(int)$result['wales'])));
			$array[4]=array("c"=>array("0"=>array("v"=>"Scotland","f"=>NULL),"1"=>array("v"=>(int)$result['scotland'])));

//Full JSON format as required by Google Charts API - these paramters will be passed into the chart in order to produce it on the page
//otherwise return null
			echo $format = "{
				\"cols\": [
				{\"id\":\"\",\"label\":\"Country\",\"pattern\":\"\",\"type\":\"string\"},
				{\"id\":\"\",\"label\":\"Count\",\"pattern\":\"\",\"type\":\"number\"},
				],
				\"rows\":".json_encode($array)."}";
		}
		else 
		{
			echo json_encode('null');
		}	
	}
	//close connection to database
	$conn->close();
}
//else if group by sentiment has been supplied from form search page form
else if ($option == 2) 
{
    //result will be equal to each row in the database containing a sentiment value until none are left
	if ($result = mysqli_fetch_array($results))
	{
	    //if the results from each sentiment value searched within the database is greater than 0
		if((int)$result['pos'] != 0 || (int)$result['neg'] != 0 || (int)$result['neu'] != 0)
		{
		    //allocate individual array slots
			$array[0]=array("c"=>array("0"=>array("v"=>"Positive","f"=>NULL),"1"=>array("v"=>(int)$result['pos'])));
			$array[1]=array("c"=>array("0"=>array("v"=>"Negative","f"=>NULL),"1"=>array("v"=>(int)$result['neg'])));
			$array[2]=array("c"=>array("0"=>array("v"=>"Neutral","f"=>NULL),"1"=>array("v"=>(int)$result['neu'])));
//Full JSON format as required by Google Charts API - these paramters will be passed into the chart in order to produce it on the page
			echo $format = "{
				\"cols\": [
				{\"id\":\"\",\"label\":\"Country\",\"pattern\":\"\",\"type\":\"string\"},
				{\"id\":\"\",\"label\":\"Count\",\"pattern\":\"\",\"type\":\"number\"},
				],
				\"rows\":".json_encode($array)."}";
		}
		else 
		{
			echo json_encode('null');
		}	
	}
	//close connection
	$conn->close();
}

//else if group by stance has been supplied from form search page form
else if ($option == 3) 
{
	if ($result = mysqli_fetch_array($results))
	{
	    //if results for anti or pro brexit are greater than 0
		if((int)$result['ex'] != 0 || (int)$result['stay'] != 0)
		{
		    //allocate the individual array slots
			$array[0]=array("c"=>array("0"=>array("v"=>"Pro-Brexit","f"=>NULL),"1"=>array("v"=>(int)$result['ex'])));
			$array[1]=array("c"=>array("0"=>array("v"=>"Pro-Stay","f"=>NULL),"1"=>array("v"=>(int)$result['stay'])));

           //JSON Google charts format
			echo $format = "{
				\"cols\": [
				{\"id\":\"\",\"label\":\"Country\",\"pattern\":\"\",\"type\":\"string\"},
				{\"id\":\"\",\"label\":\"Count\",\"pattern\":\"\",\"type\":\"number\"},
				],
				\"rows\":".json_encode($array)."}";
		}
		else 
		{
			echo json_encode('null');
		}
	}
	$conn->close();
}
else
{
    //return null close the connection
	echo json_encode('null');
	$conn->close();
}

?>

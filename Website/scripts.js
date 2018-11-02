    function checkValid()
   {
   	 //Function ensures that at least one form value equals "All" and that two form values don't both equal "All"
   	 var canDraw = false;
   	 var cantdraw = false;
     if (document.getElementById("location").value == "All")
     {
       canDraw = true;
     } 
     if (document.getElementById("sentiment").value == "All")
     {
       if(canDraw == false)
       {
       	canDraw = true;
       }
       else
       {
       	cantdraw = true;
       }
     }
     if (document.getElementById("stance").value == "All")
     {
       if(canDraw == false)
       {
       	canDraw = true;
       }
       else
       {
       	cantdraw = true;
       }
     } 
     if(cantdraw == false && canDraw == true)
     {
       drawC();
       hide_div('invalidForm');
     }
     else
     {
       show_div('invalidForm');
     }
   }
    //Used to determine which graph to draw next, and where to draw it
    function drawC(nextGraph, div){
      if (nextGraph == "barchart")
      {
        drawBarChart("none", div);
      }
      if (nextGraph == "piechart")
      {
        drawPieChart("none", div);
      }
    }
    //General purpose hiding message and div code
    function hide_div(arg){
      var x = document.getElementById(arg);
      x.style.display = 'none';
    }
    function show_div(arg){
      var x = document.getElementById(arg);
      x.style.display = 'block';
    }
    function hide(arg){
      var x = document.getElementById(arg);
      x.disabled = true;
    }
    function show(arg){
      var x = document.getElementById(arg);
      x.disabled = false;
    }
    function hide_p(arg)
    {
      var x = document.getElementById(arg);
      x.hidden = true;
    }
    function show_p(arg)
    {
      var x = document.getElementById(arg);
      x.hidden = false;
    }
    //function to draw a map, the argument is where the map is to be drawn
    function drawMap(arg1) 
    {
      //Ajax used to get the data from the php script
      var jsonData = $.ajax({
              url: "map.php",
              dataType: "json",
              title: "World map showing number of tweets regarding brexit from each country",
              async: false //Ensures script doesn't continue on until data is received
              }).responseText;
      if (jsonData != "\"null\"")
      {
        var data =  new google.visualization.DataTable(jsonData);
        var options = {
        showTooltip: true,
        showInfoWindow: true
        };
        var map = new google.visualization.Map(document.getElementById(arg1));
        map.draw(data, options);
      }
   }
    function drawCalendarChart(arg1) //Argument tells function where to draw chart
     {
         var jsonData = $.ajax({
              url: "tweets_by_day.php",
              dataType: "json",
              async: false
              }).responseText;
         var options = {
           title: "Tweets by day",
           height: 750,
           calendar: {cellSize: 15},
         };
         if (jsonData != "\"null\"")
         {
            var data = new google.visualization.DataTable(jsonData);
            var chart = new google.visualization.Calendar(document.getElementById(arg1));
            chart.draw(data, options);
         }
   }
   var firstBar = true; //Used to check if first time bar chart is being drawn
   						//If true, default values are used else values supplied by user are used
   function drawBarChart(arg1, arg2) //Argument 1 = Country Argument 2 = Where to draw graph
    {
      if (firstBar == true)
      {
        firstBar = false; //No longer first time function is run
         if (arg1 == "All")
            {
              var jsonData = $.ajax({url: "form_retrieval.php",
              type:"POST",
              data: { country : arg1, sentiment : sent, stance : stan, search_string: search_str},
              dataType: "json",
              async: false
              }).responseText;
            }
            //Arg1 will be a country, and sentiment is made the group by variable if called from international html
            if (arg1 != "All")
            {
              var jsonData = $.ajax({url: "form_retrieval.php",
              type:"POST",
              data: { country : arg1, sentiment : "All", stance : stan, search_string: search_str},
              dataType: "json",
              async: false
              }).responseText;
            }
        if (jsonData != "\"null\"")
        {
          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);
          if (arg1 == "All")
          {
          	var options = {
          	title: "Percentage of Tweets split by country",
           backgroundColor: '#fcfbfb'
            };
          }
          if (arg1 != "All")
          {
            var options = {
          	  title: "Percentage of Tweets split by sentiment",
              backgroundColor: '#fcfbfb'
              };
          }
          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.ColumnChart(document.getElementById(arg2));
          chart.draw(data, options);
          if(arg2 != "index_barchart_div") //Check if script called from index page or not
          {								   //This will be repeated in this function and in drawPieChart function
	         hide_p('no_val'); //Hide p only if not from index page, as index page doesn't need this warning
          }
        }
        else
        {
          scroll(0,0) //scroll to top of page where error is displayed
        }
    }
    else
    {
      //This part gets the values from the form to pass to the php script
      if(document.getElementById("location").disabled != true)
      {
      	var graph_name = ""; //This will be used as the title of the graph. It varies depending on user input to form.
      	var and = 0; // If and = 2 then an and is needed inside the statement
        var ctry;
        ctry = document.getElementById("location").value;
        if(ctry == "All")
        {
          graph_name = "Percentage of Tweets split by country";
        }
        
        else if(ctry == "Choose Region:" || ctry == "Choose Country:")
        {
          ctry = "none";
        }
      	
      	if(ctry != "none" && ctry != "All")
      	{
      	  graph_name = " that are sent from " + ctry + " \n"; 
      	  and = 1;
      	}
      }
      if(document.getElementById("searchbox").disabled != true)
      {
        var search_str;
        search_str = document.getElementById("searchbox").value;
      }
      if(document.getElementById("sentiment").disabled != true)
      {
        var sent;
        sent = document.getElementById("sentiment").value;
        if(sent == "All")
        {
        	graph_name = "Percentage of Tweets split by sentiment" + graph_name;
        }
        else if(sent == "Choose Sentiment:")
        {
          sent = "none";
        }
      	if(sent != "none" && sent != "All")
      	{
      		  if(sent == "pos")
      		  	str_sent = "positive";
      		  else if(sent == "neg")
      		  	str_sent = "negative";
      		  else if(sent == "neu")
      		  	str_sent = "neutral";
      		  graph_name += "\nthat are " + str_sent; 
      		  and++;
      	}
      }
      if(document.getElementById("stance").disabled != true)
      {
        var stan;
        stan = document.getElementById("stance").value;
        if(stan == "All")
        {
        	graph_name = "Percentage of Tweets split by stance" + graph_name;
        }
        else if(stan == "Choose Stance:")
        {
          stan = "none";
        }
        if(stan != "none" && stan != "All")
      	{
      		  if(stan == "Pro_stay")
      		  	str_stan = "pro stay";
      		  else
      		  	str_stan = "pro brexit";
      		  graph_name += "\nthat are " + str_stan; 
      		  and++;
      	}
      }
      if(and == 2) //Replace new line with and, where there are 3 statements in the sentence. Grammatical purposes.
      {
      	graph_name = graph_name.replace("\n", "and ");
      }
      var jsonData = $.ajax({

          url: "form_retrieval.php",
          type:"POST",
          data: { country : ctry, sentiment : sent, stance : stan, search_string : search_str},
          dataType: "json",
          async: false
          }).responseText;
      if (jsonData != "\"null\"")
      {
        // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable(jsonData);
        var options = {
           title: graph_name,
           backgroundColor: '#fcfbfb'
            };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.ColumnChart(document.getElementById(arg2));
        chart.draw(data, options);
        if(arg2 != "index_barchart_div") //Check if script called from index page or not
          {
	         hide_p('no_val'); //Hide p only if not from index page
          }
      }
      else
      {
        scroll(0,0);
        if(arg2 != "index_barchart_div") //Check if script called from index page or not
          {
	         show_p('no_val'); //Show p only if not from index page
          }
      }
    }
  }
  var first = true;
  //Arg1 is the variable to group by for the chart on load
  //Arg2 is the div to which to draw the graph
  function drawPieChart(arg1, arg2) 
  {   
      if (first == true)
      {
          first = false;
          //Arg1 will be the variable to group by if being called from uk html
          
            if (arg1 == "All")
            {
              var jsonData = $.ajax({url: "form_retrieval.php",
              type:"POST",
              data: { country : arg1, sentiment : sent, stance : stan, search_string: search_str},
              dataType: "json",
              async: false
              }).responseText;
            }
            //Arg1 will be a country, and sentiment is made the group by variable if called from international html
            if (arg1 != "All")
            {
              var jsonData = $.ajax({url: "form_retrieval.php",
              type:"POST",
              data: { country : arg1, sentiment : "All", stance : stan, search_string: search_str},
              dataType: "json",
              async: false
              }).responseText;
            }
        if (jsonData != "\"null\"")
        {
          // Create our data table out of JSON data loaded from server.
          var data = new google.visualization.DataTable(jsonData);
          if (arg1 == "All")
          {
	          var options = {
	          		title: "Percentage of Tweets split by country",
	                is3D: true,
	         		slices: {0: {color: '#377eb8'}, 1:{color: '#e41a1c'}, 2:{color:'#4daf4a'}},
	         		backgroundColor: '#fcfbfb'
	          };
	      }
	      if (arg1 != "All")
	      {
	      	 var options = {
	      	 		title: "Percentage of Tweets split by sentiment",
	                is3D: true,
	         		slices: {0: {color: '#377eb8'}, 1:{color: '#e41a1c'}, 2:{color:'#4daf4a'}},
	        		backgroundColor: '#fcfbfb'
	          };
	      }
          // Instantiate and draw our chart, passing in some options.
          var chart = new google.visualization.PieChart(document.getElementById(arg2));
          chart.draw(data, options);
          if(arg2 != "index_piechart_div") //Check if script called from index page or not
          {
	         hide_p('no_val'); //Hide p only if not from index page
          }
        }
        else
        {
          scroll(0,0);
        }
    }
    else
    {
      if(document.getElementById("location").disabled != true)
      {
      	var graph_name = ""; //This will be used as the title of the graph. It varies depending on user input to form.
      	var and = 0; // If and = 2 then an and is needed in the statement
        var ctry;
        ctry = document.getElementById("location").value;
        if(ctry == "All")
        {
          graph_name = "Percentage of Tweets split by country";
        }
        
        else if(ctry == "Choose Region:" || ctry == "Choose Country:")
        {
          ctry = "none";
        }
      	
      	if(ctry != "none" && ctry != "All")
      	{
      	  graph_name = " that are sent from " + ctry + " \n"; 
      	  and = 1;
      	}
      }
      if(document.getElementById("searchbox").disabled != true)
      {
        var search_str;
        search_str = document.getElementById("searchbox").value;
      }
      if(document.getElementById("sentiment").disabled != true)
      {
        var sent;
        sent = document.getElementById("sentiment").value;
        if(sent == "All")
        {
        	graph_name = "Percentage of Tweets split by sentiment" + graph_name;
        }
        else if(sent == "Choose Sentiment:")
        {
          sent = "none";
        }
      	if(sent != "none" && sent != "All")
      	{
      		  if(sent == "pos")
      		  	str_sent = "positive";
      		  else if(sent == "neg")
      		  	str_sent = "negative";
      		  else if(sent == "neu")
      		  	str_sent = "neutral";
      		  graph_name += "\nthat are " + str_sent; 
      		  and++;
      	}
      }
      if(document.getElementById("stance").disabled != true)
      {
        var stan;
        stan = document.getElementById("stance").value;
        if(stan == "All")
        {
        	graph_name = "Percentage of Tweets split by stance" + graph_name;
        }
        else if(stan == "Choose Stance:")
        {
          stan = "none";
        }
        if(stan != "none" && stan != "All")
      	{
      		  if(stan == "Pro_stay")
      		  	str_stan = "pro stay";
      		  else
      		  	str_stan = "pro brexit";
      		  graph_name += "\nthat are " + str_stan; 
      		  and++;
      	}
      }
      if(and == 2)
      {
      	graph_name = graph_name.replace("\n", "and ");
      }
      var jsonData = $.ajax({

          url: "form_retrieval.php",
          type:"POST",
          data: { country : ctry, sentiment : sent, stance : stan, search_string : search_str},
          dataType: "json",
          async: false
          }).responseText;
      if (jsonData != "\"null\"")
      {
        // Create our data table out of JSON data loaded from server.
        var data = new google.visualization.DataTable(jsonData);
        var options = {
        	 title: graph_name,
             is3D: true,
             slices: {0: {color: '#377eb8'}, 1:{color: '#e41a1c'}, 2:{color:'#4daf4a'}},
             backgroundColor: '#fcfbfb'
        };

        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.PieChart(document.getElementById(arg2));
        chart.draw(data, options);
        if(arg2 != "index_piechart_div") //Check if script called from index page or not
          {
	         hide_p('no_val'); //Hide p only if not from index page
          }
      }
      else
      {
        scroll(0,0);
        if(arg2 != "index_piechart_div") //Check if script called from index page or not
          {
	         show_p('no_val'); //Show p only if not from index page
          }
      }
    }
  }
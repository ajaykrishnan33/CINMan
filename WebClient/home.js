$(document).ready(function(){
	var authToken = localStorage.getItem("authToken");
	var machines = [];
	var users = [];
	var logs = [];
	var host = "localhost";
	var port = "8000";
	$("#login").submit(function(){
  /*function to check userid & password*/
	      //var $form = form;
	      //var serializedDatal $(this).serialize();
	      var username=$("#userid").val();
	      var password=$("#pswrd").val();
          $.ajax
	      ({
	        type: "POST",
	        url: "http://"+host+":"+port+"/api-token-auth/",
	       dataType: 'json',
	       async: false,
           data: {"username":username,"password":password},
	       success: function (response){
	    	//console.log(response);
	    	// alert(response["token"]);
	    	authToken = response["token"];
	    	
	    	//console.log(localStorage.getItem("authToken"));
	    	$("#machines").show();
	    	$("#users").show();
	    	$("#activity").show();
	    	$("#well").html("");
	    	$("#heading").text("Machine List");
	    	   $.ajax
			  ({
			    type: "GET",
			    url: "http://"+host+":"+port+"/app/machine/",
			    dataType: 'json',
			    async: false,
			    beforeSend: function (xhr) {
				    xhr.setRequestHeader ("Authorization", "Token " + authToken);
				},
			    success: function (response){
			    	//console.log(response);
			    	$("#well").append("<input type='text' id='search' name='search' class='form-control' style='margin-bottom:5px;width:250px;' placeholder='Search by Machine I.P.'><div id='subwell'></div>");
			    	for(machine in response){
			    		//console.log(machine);
			    		machines.push(response[machine]);
			    		if(response[machine]["active"])
			    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:green;cursor:pointer;'>"+response[machine]["ip_address"]+"</a></div></div>");
			    		else
			    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:red;cursor:pointer'>"+response[machine]["ip_address"]+"</a></div></div>");
			    	}
			    }
			});
			  $.ajax
				  ({
				    type: "GET",
				    url: "http://"+host+":"+port+"/app/machineuser/",
				    dataType: 'json',
				    async: false,
				    beforeSend: function (xhr) {
					    xhr.setRequestHeader ("Authorization", "Token " + authToken);
					},
				    success: function (response){
				    	//console.log(response);
				    	for(user in response){
				    		console.log(user);
				    		users.push(response[user]);
				    		}		    		
				    }
				});
	    	
	    	  	},
	    	  	error:function(response){
	    	  		$("#heading").text("Login Failed");
	    	  	}
	      });
	});
 

	$("#machines").click(function(){
		$("#well").html("");
		$("#heading").text("Machine List");
		machines=[];
		$.ajax
		  ({
		    type: "GET",
		    url: "http://"+host+":"+port+"/app/machine/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	//console.log(response);
		    	$("#well").append("<input type='text' id='search' name='search' class='form-control' style='margin-bottom:5px;width:250px;' placeholder='Search by Machine I.P.'><div id='subwell'></div>");
		    	for(machine in response){
		    		console.log(machine);
		    		machines.push(response[machine]);
		    		if(response[machine]["active"])
		    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:green;cursor:pointer;'>"+response[machine]["ip_address"]+"</a></div></div>");
		    		else
		    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:red;cursor:pointer'>"+response[machine]["ip_address"]+"</a></div></div>");
		    	}
		    }
		});
	});

	$("#users").click(function(){
		$("#well").html("");
		$("#heading").text("User List");
		users=[];
		$.ajax
		  ({
		    type: "GET",
		    url: "http://"+host+":"+port+"/app/machineuser/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	//console.log(response);
		    	for(user in response){
		    		console.log(user);
		    		users.push(response[user]);
		    		$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='user' data-id="+response[user]["id"]+" style='color:green;cursor:pointer;'>"+response[user]["name"]+"</a></div></div>");		    	}
		    }
		});
	});

	$("#activity").click(function(){
		$("#well").html("");
		$("#heading").text("Activity Logs");
		
		var flag = true;
		callback();
		setInterval(callback, 5000);
		function callback(){
			logs=[];
			console.log("Trying...");
			$.ajax
			  ({
			    type: "GET",
			    url: "http://"+host+":"+port+"/app/logentry/",
			    dataType: 'json',
			    async: false,
			    beforeSend: function (xhr) {
				    xhr.setRequestHeader ("Authorization", "Token " + authToken);
				    $("#ips").html("");
				},
			    success: function (response){
			    	console.log(response);
			    	if(flag)
			    		$("#well").append("<div class='dropdown'><button class='btn btn-primary dropdown-toggle' type='button' data-toggle='dropdown'>Select Machine I.P.<span class='caret'></span></button><ul id='ips' class='dropdown-menu'></ul></div><div id='logs'></div>");			    	
			    	flag=false;
			    	for(machine in machines){
			    		$("#ips").append("<li><a id='iplog' data-id="+machines[machine]["id"]+" href='#'>"+machines[machine]["ip_address"]+"</a></li>");
			    	}
			    	for(log in response){
			    		logs.push(response[log]);
			    	}
			    }
			});
		}
	});

	$(document).on("click","#activity2",function(){
		var dat_id = $(this).attr("data-id");
		$("#well").html("<div id='logs'><button type='button' id='activity2' data-id="+dat_id+" class='btn btn-primary'><span class='glyphicon glyphicon-refresh'></span></button></div>");
		$("#heading").text("Activity Logs");
		
		var flag = true;
		callback();
		//setInterval(callback, 5000);
		function callback(){
			logs=[];
			$("#well").html("<div id='logs'><button type='button' id='activity2' data-id="+dat_id+" class='btn btn-primary'><span class='glyphicon glyphicon-refresh'></span></div>");
			console.log("Trying...");
			$.ajax
			  ({
			    type: "GET",
			    url: "http://"+host+":"+port+"/app/logentry/?machine="+dat_id,
			    dataType: 'json',
			    async: false,
			    beforeSend: function (xhr) {
				    xhr.setRequestHeader ("Authorization", "Token " + authToken);
				},
			    success: function (response){
			    	console.log(response);
			    	for(log in response){
			    		logs.push(response[log]);
			    	}
			    	for(mac in logs){
							if(logs[mac]['severity']<2)
								$("#logs").append("<p style='color:green'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
							if(logs[mac]['severity']===2)
								$("#logs").append("<p style='color:yellow'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
							if(logs[mac]['severity']>2)
								$("#logs").append("<p style='color:red'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
					}
			    }
			});
		}
	});

	$(document).on("input","#search",function(){
		console.log("cu,");
		$("#subwell").html("");
		var machinesX = [];
		var inputval = $("#search").val();
		for(mac in machines){
			if(machines[mac]["ip_address"].search(inputval)>-1)
				machinesX.push(machines[mac]);
		}
		for(machine in machinesX){
    		if(machinesX[machine]["active"])
    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+machinesX[machine]["id"]+" style='color:green;cursor:pointer;'>"+machinesX[machine]["ip_address"]+"</a></div></div>");
    		else
    			$("#subwell").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+machinesX[machine]["id"]+" style='color:red;cursor:pointer'>"+machinesX[machine]["ip_address"]+"</a></div></div>");
    	}
	});

	$(document).on("click","#machine",function(){
		$("#well").html("");
		$("#heading").text("Machine Details");
		var req = 0;
		var man = parseInt($(this).attr("data-id"));
		var manx = "";
		for(mac in machines){
			manx = machines[mac]["id"] 
			if(manx===man){
				req=mac;
				break;
			}
		}
		console.log(machines[req])
		//$("#well").text(machines[req]);
		var req_mac = machines[req];
		$("#well").html("<button type='button' id='activity2' class='btn btn-primary' data-id="+req_mac["id"]+" >View Machine Activity</button><div style='padding: 10px;'><img style='display: inline-block;height: 50px;width: 68px' src='http://www.clipartkid.com/images/74/monitor-clip-art-at-clker-com-vector-clip-art-online-royalty-free-h2yVSl-clipart.png'><h4 style='display: inline-block;margin-left: 75px;'>"+req_mac["ip_address"]+"</h4></div><li>Active:"+req_mac["active"]+"</li><li>MAC Address:"+req_mac["mac_address"]+"</li><li>CPU Speed:"+req_mac["cpu_speed"]+"</li><li>HardDisk Description:"+req_mac["ram_capacity"]+"</li><li>HardDisk Capacity:"+req_mac["harddisk_capacity"]+"</li>");
		$("#well").append("<li>Logged In UserIds:</li>")
		for(x in req_mac["last_logged_in_users"]){
			$("#well").append("<p data-id="+req_mac['last_logged_in_users'][x]+" style='cursor:pointer;' id='user'>      "+req_mac['last_logged_in_users'][x]+"</p>")
		}
		if(req_mac["last_logged_in_users"].length===0)
			$("#well").append("<p style='cursor:pointer;'>None</p>")			
		$("#well").append("<li>Installed Softwares:</li>")
		for(x in req_mac["installed_softwares"]){
			$("#well").append("<p data-id="+req_mac['installed_softwares'][x]+" id='software'>      "+req_mac['installed_softwares'][x]+"</p>")
		}
		if(req_mac["installed_softwares"].length===0)
			$("#well").append("<p style='cursor:pointer;'>None</p>")
	});

	$(document).on("click","#user",function(){
		$("#well").html("");
		$("#heading").text("User Details");
		var req = 0;
		var man = parseInt($(this).attr("data-id"));
		var manx = "";
		for(mac in users){
			manx =users[mac]["id"] 
			if(manx===man){
				req=mac;
				break;
			}
		}
		console.log(users[req])
		var req_mac = users[req];
		$("#well").html("<div style='padding: 10px;'><img style='display: inline-block;height: 68px;width: 68px' src='https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQXhqsqwmN807b9fGFbGa4xk_8mPSirTe13ZmXIgml6LD3lst2xv2MB2Q'><h4 style='display: inline-block;margin-left: 75px;'>"+req_mac["name"]+"</h4></div><li>Currently Logged In:"+req_mac["currently_logged"]+"</li><li>Failed Logins:"+req_mac["failed_login_count"]+"</li><li>Last Failed Login date:"+req_mac["last_failed_login_date"]+"</li><li>Last Login Date:"+req_mac["last_logged_in_date"]+"</li><li>Suspicious Activity Count:"+req_mac["suspicious_activity_count"]+"</li>");
		$("#well").append("<li>Login Sessions:</li>")
		for(x in req_mac["login_sessions"]){
			$("#well").append("<p data-id="+req_mac['login_sessions'][x]+" style='cursor:pointer;' id='machine'>      "+req_mac['login_sessions'][x]+"</p>")
		}
		if(req_mac["login_sessions"].length===0)
			$("#well").append("<p style='cursor:pointer;'>None</p>")
	});

	$(document).on("click","#iplog",function(){
		$("#well").html("<div class='dropdown'><button class='btn btn-primary dropdown-toggle' type='button' data-toggle='dropdown'>Select Machine I.P.<span class='caret'></span></button><ul id='ips' class='dropdown-menu'></ul></div><div id='logs'></div>");
		for(machine in machines){
			    		$("#ips").append("<li><a id='iplog' data-id="+machines[machine]["id"]+" href='#'>"+machines[machine]["ip_address"]+"</a></li>");
			    	}
		$("#logs").append("<h3>Showing logs for Machine "+$(this).text()+"</h3>")
		var req = 0;
		var man = parseInt($(this).attr("data-id"));
		var manx = "";
		for(mac in logs){
			manx = parseInt(logs[mac]["machine"]) ;
			if(manx===man){
				if(logs[mac]['severity']<2)
					$("#logs").append("<p style='color:green'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
				if(logs[mac]['severity']===2)
					$("#logs").append("<p style='color:yellow'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
				if(logs[mac]['severity']>2)
					$("#logs").append("<p style='color:red'>"+logs[mac]['timestamp']+" : "+logs[mac]['text']+"</p>");
			}
		}
	});
});

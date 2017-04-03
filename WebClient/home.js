$(document).ready(function(){
	var authToken = "7f10607a9f14e83cb5a4bab9b4e77dc83faa89f5";
	var machines = [];
	var users = [];
    $.ajax
	  ({
	    type: "GET",
	    url: "http://localhost:8000/app/machine/",
	    dataType: 'json',
	    async: false,
	    beforeSend: function (xhr) {
		    xhr.setRequestHeader ("Authorization", "Token " + authToken);
		},
	    success: function (response){
	    	//console.log(response);
	    	for(machine in response){
	    		//console.log(machine);
	    		machines.push(response[machine]);
	    		if(response[machine]["active"])
	    			$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:green;cursor:pointer;'>"+response[machine]["ip_address"]+"</a></div></div>");
	    		else
	    			$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:red;cursor:pointer'>"+response[machine]["ip_address"]+"</a></div></div>");
	    	}
	    }
	});
	  $.ajax
		  ({
		    type: "GET",
		    url: "http://localhost:8000/app/machineuser/",
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

	$("#machines").click(function(){
		$("#well").html("");
		$("#heading").text("Machine List");
		machines=[]
		$.ajax
		  ({
		    type: "GET",
		    url: "http://localhost:8000/app/machine/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	//console.log(response);
		    	for(machine in response){
		    		console.log(machine);
		    		machines.push(response[machine]);
		    		if(response[machine]["active"])
		    			$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:green;cursor:pointer;'>"+response[machine]["ip_address"]+"</a></div></div>");
		    		else
		    			$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='machine' data-id="+response[machine]["id"]+" style='color:red;cursor:pointer'>"+response[machine]["ip_address"]+"</a></div></div>");
		    	}
		    }
		});
	});

	$("#users").click(function(){
		$("#well").html("");
		$("#heading").text("User List");
		$.ajax
		  ({
		    type: "GET",
		    url: "http://localhost:8000/app/machineuser/",
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
		    		$("#well").append("<div class='panel panel-info' style='margin-bottom: 5px;'><div class='panel-body' style='text-align: center;'><p id='user' data-id="+response[user]["id"]+" style='color:green;cursor:pointer;'>"+response[user]["username"]+"</a></div></div>");		    	}
		    }
		});
	});

	$("#activity").click(function(){
		$("#well").html("");
		$("#heading").text("Activity Logs");
		$.ajax
		  ({
		    type: "GET",
		    url: "http://localhost:8000/app/machine/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	//console.log(response);
		    	$("#well").append("<div class='dropdown'><button class='btn btn-primary dropdown-toggle' type='button' data-toggle='dropdown'>Select Machine I.P.<span class='caret'></span></button><ul id='ips' class='dropdown-menu'></ul></div><div id='logs'></div>");
		    	for(machine in machines){
		    		$("#ips").append("<li><a id='iplog' data-id="+machines[machine]["id"]+" href='#'>"+machines[machine]["ip_address"]+"</a></li>");
		    	}
		    }
		});
	});


	$(document).on("click","#machine",function(){
		$("#well").html("");
		$("#heading").text("Machine Details");
		var req = 0;
		var man = parseInt($(this).attr("data-id"));
		var manx = "";
		for(mac in machines){
			manx =machines[mac]["id"] 
			if(manx===man){
				req=mac;
				break;
			}
		}
		console.log(machines[req])
		//$("#well").text(machines[req]);
		var req_mac = machines[req];
		$("#well").html("<div style='padding: 10px;'><img style='display: inline-block;height: 50px;width: 68px' src='http://www.clipartkid.com/images/74/monitor-clip-art-at-clker-com-vector-clip-art-online-royalty-free-h2yVSl-clipart.png'><h4 style='display: inline-block;margin-left: 75px;'>"+req_mac["ip_address"]+"</h4></div><li>Active:"+req_mac["active"]+"</li><li>MAC Address:"+req_mac["mac_address"]+"</li><li>CPU Speed:"+req_mac["cpu_speed"]+"</li><li>HardDisk Description:"+req_mac["ram_capacity"]+"</li><li>HardDisk Capacity:"+req_mac["harddisk_capacity"]+"</li>");
		$("#well").append("<li>Logged In UserIds:</li>")
		for(x in req_mac["last_logged_in_users"]){
			$("#well").append("<p data-id="+req_mac['last_logged_in_users'][x]+" style='cursor:pointer;' id='user'>      "+req_mac['last_logged_in_users'][x]+"</p>")
		}
		$("#well").append("<li>Installed Softwares:</li>")
		for(x in req_mac["installed_softwares"]){
			$("#well").append("<p data-id="+req_mac['installed_softwares'][x]+" id='software'>      "+req_mac['installed_softwares'][x]+"</p>")
		}
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
		$("#well").html("<div style='padding: 10px;'><img style='display: inline-block;height: 68px;width: 68px' src='https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQXhqsqwmN807b9fGFbGa4xk_8mPSirTe13ZmXIgml6LD3lst2xv2MB2Q'><h4 style='display: inline-block;margin-left: 75px;'>"+req_mac["username"]+"</h4></div><li>Currently Logged In:"+req_mac["currently_logged"]+"</li><li>Failed Logins:"+req_mac["failed_login_count"]+"</li><li>Last Failed Login date:"+req_mac["last_failed_login_date"]+"</li><li>Last Login Date:"+req_mac["last_logged_in_date"]+"</li><li>Suspicious Activity Count:"+req_mac["suspicious_activity_count"]+"</li>");
		$("#well").append("<li>Login Sessions:</li>")
		for(x in req_mac["login_sessions"]){
			$("#well").append("<p data-id="+req_mac['login_sessions'][x]+" style='cursor:pointer;' id='machine'>      "+req_mac['login_sessions'][x]+"</p>")
		}
	});

	$(document).on("click","#iplog",function(){
		$("#logs").html("");
		$("#logs").append("<h3>Showing logs for Machine "+$(this).text()+"</h3>")
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
		var req_mac = machines[req];
		for(x in req_mac["machine_logs"]){
			$("#logs").append("<p>"+req_mac['machine_logs'][x]+"</p>")
		}
	});
});

$(document).ready(function(){
	var authToken = localStorage.getItem("authToken");
	console.log(authToken);
	$("#usernaam").text(localStorage.getItem("username"));
		var host = localStorage.getItem("host");
	var port = localStorage.getItem("port");

	var alerts = [];

	callback();
	callback2();
	//setInterval(callback, 5000);

	function callback2(){
		$.ajax
		  ({
		    type: "GET",
		    url: "http://"+host+":"+port+"/app/alert/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	console.log(response);
		    	//fa-eercast
		    	$("#numalerts").text(Math.min(response["count"],10));
			    for(var i=0;i<Math.min(response["count"],10);i++){
			    	alerts.push(response["results"][i]["text"]);
					localStorage.setItem("last-machine-id",response["results"][i]["machines"][0]["id"])
					$("#alerts-drp").append('<li class="message-preview"><a href="activity.html"><span class="avatar"><i class="fa fa-bell"></i></span><span class="message">'+response["results"][i]["text"]+"("+response["results"][i]["machines"][0]["ip_address"]+")"+'</span></a></li><li class="divider"></li>'); 	
			    }
			    $("#alerts-drp").append('<li><a href="alerts.html">Go to Alerts</a></li>');
			}
		});
	}

	function callback(){
		var machines = [];
		var users = [];
		$('#page-wrapper2').html("");
		
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
		    	for(machine in response){
		    		console.log(machine);
		    		machines.push(response[machine]);
		    		if(response[machine]["active"])
		    			$("#page-wrapper2").append("<button type='button' class='btn btn-default btn-lg btn-block'><p id='machine' data-id="+response[machine]["id"]+" style='color:green;cursor:pointer;'><strong>"+response[machine]["host_name"]+"("+response[machine]["ip_address"]+")"+"</strong></p></button>");
		    		else
		    			$("#page-wrapper2").append("<button type='button' class='btn btn-default btn-lg btn-block'><p id='machine' data-id="+response[machine]["id"]+" style='color:red;cursor:pointer;'><strong>"+response[machine]["host_name"]+"("+response[machine]["ip_address"]+")"+"</strong></p></button>");
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
		
	}

	$(document).on("input","#search",function(){
		console.log("cu,");
		$("#page-wrapper2").html("");
		var machinesX = [];
		var inputval = $("#search").val();
		for(mac in machines){
			if(machines[mac]["host_name"].search(inputval)>-1 || machines[mac]["ip_address"].search(inputval)>-1)
				machinesX.push(machines[mac]);
		}
		for(machine in machinesX){
    		if(machinesX[machine]["active"])
    			$("#page-wrapper2").append("<button type='button' class='btn btn-default btn-lg btn-block'><p id='machine' data-id="+machinesX[machine]["id"]+" style='color:green;cursor:pointer;'><strong>"+machinesX[machine]["host_name"]+"("+machinesX[machine]["ip_address"]+")"+"</strong></p></button>");
	    	else
	    		$("#page-wrapper2").append("<button type='button' class='btn btn-default btn-lg btn-block'><p id='machine' data-id="+machinesX[machine]["id"]+" style='color:red;cursor:pointer;'><strong>"+machinesX[machine]["host_name"]+"("+machinesX[machine]["ip_address"]+")"+"</strong></p></button>");    	}
	});

	$(document).on("click","#machine",function(){
		localStorage.setItem("last-machine-id",$(this).attr("data-id"));
		window.location = 'machine.html';
	});

	bootstrap_alert = function () {}
	bootstrap_alert.warning = function (message, alert, timeout) {
	    $('<div id="floating_alert" style="position: absolute;top: 20px;right: 20px;z-index: 5000;" class="alert alert-' + alert + ' fade in"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>' + message + '&nbsp;&nbsp;</div>').appendTo('body');


	    setTimeout(function () {
	        $(".alert").alert('close');
	    }, timeout);

	}

	var ws4redis = WS4Redis({
        uri: "ws://"+host+":"+port+"/ws/foobar?subscribe-broadcast&publish-broadcast&echo",
        connecting: on_connecting,
        connected: on_connected,
        receive_message: receiveMessage,
        disconnected: on_disconnected
    });

    // attach this function to an event handler on your site
    function sendMessage() {
        ws4redis.send_message('A message');
    }

    function on_connecting() {
        //alert('Websocket is connecting...');
    }

    function on_connected() {
        //ws4redis.send_message('Hello');
    }

    function on_disconnected(evt) {
        //alert('Websocket was disconnected: ' + JSON.stringify(evt));
    }

    // receive a message though the websocket from the server
    function receiveMessage(msg) {
        //alert('Message from Websocket: ' + msg);
        console.log(msg);
        if(msg.indexOf("Machine")==0)
        	callback();
        else if(msg.indexOf("Alert:")==0)
        {
        	$("#alerts-drp").html("");
        	bootstrap_alert.warning(msg.substr(6), 'warning', 4000);
        	alerts.unshift(msg.substr(6));
        	callback2();
        }
     //    $("#alert").alert();
     //    $("#alert-text").text(msg);
     //    var alertsX = []
     //    for(var i=0;i<12;i++){
     //    	alertsX.push(alerts[i]);
     //    }
     //    alerts = [];
     //    for(var i=1;i<12;i++){
     //    	alerts.push(alertsX[i])
     //    }
     //    alerts.push(msg);
     //    $('#alertbar').html("");
     //    for(var i=0;i<12;i++)
	    // 	{
	    // 		$("#alertbar").append("<li style='height:8.3%;padding:5px;text-align:center;border-bottom:2px solid white;color:white'>"+alerts[i]+"</li>");
	    // 	}
	    // $("#alert").fadeTo(10000, 500).slideUp(500, function(){
     //       $("#alert").slideUp(500);
     //    });
    }

});
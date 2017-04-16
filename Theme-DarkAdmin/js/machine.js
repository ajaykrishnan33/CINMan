$(document).ready(function(){
	var authToken = localStorage.getItem("authToken");
	console.log(authToken);
	$("#usernaam").text(localStorage.getItem("username"));
		var host = localStorage.getItem("host");
	var port = localStorage.getItem("port");
	var userid = localStorage.getItem("last-machine-id");
	var performance = [12, 43, 34, 22, 12, 33, 4, 17, 22, 34, 54, 67],
                visits1 = [],
                visits2 = [],
                traffic = [];

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
		    	$("#numalerts").text(response["count"]);
			    for(var i=0;i<response["count"];i++){
			    	alerts.push(response["results"][i]["text"]);
					$("#alerts-drp").append('<li class="message-preview"><a href="#"><span class="avatar"><i class="fa fa-bell"></i></span><span class="message">'+response["results"][i]["text"].substr(0,7)+'...</span></a></li><li class="divider"></li>');				    	
			    }
			    $("#alerts-drp").append('<li><a href="alerts.html">Go to Alerts</a></li>');
			}
		});
	}

	function callback(){
		$('#news-list').html("");
		visits1 = [];
		visits2 = [];
		traffic = [];
		$("#shieldui-grid1").html("");

		$.ajax
		  ({
		    type: "GET",
		    url: "http://"+host+":"+port+"/app/machine/"+userid+"/",
		    dataType: 'json',
		    async: false,
		    beforeSend: function (xhr) {
			    xhr.setRequestHeader ("Authorization", "Token " + authToken);
			},
		    success: function (response){
		    	console.log(response);
		    	//fa-eercast
		    	if(response["active"])
			    	$("#ip").html(response["host_name"]+"<small><span style='margin:3px' class='label label-success'>Online</span></small>");
			    else
			    	$("#ip").html(response["host_name"]+" <small><span style='margin:3px' class='label label-danger'>Offline</span></small>");
			    for(var i=0;i<response["active_login_sessions"].length;i++)
			    	$("#news-list").append("<li><i class='fa fa-user fa-4x pull-left'></i><div class='news-item-info'><div class='name'><a href='#'>"+response["active_login_sessions"][i]["username"]+"</a></div><div class='position'>"+response["active_login_sessions"][i]["ip_address"]+"</div><div class='time'>"+response["active_login_sessions"][i]["login_time"]+"</div></div></li>");
		    	//visits1,visits2 = [parseInt(response["harddisk_description"]["available"]),parseInt(response["harddisk_description"]["used"])];
		    	var x = parseInt(response["harddisk_description"].split("\", \"used\": ")[0].split("{\"available\": \"")[1]);
		    	var y = parseInt(response["harddisk_description"].split("\", \"used\": ")[1].split(",")[0].split("\"")[1]);
		    	var x1 = parseInt(JSON.parse(response["harddisk_description"])["available"]);
		    	var y1 = parseInt(JSON.parse(response["harddisk_description"])["used"]);
		    	var x2 = parseInt(JSON.parse(response["ram_description"])["available"]);
		    	var y2 = parseInt(JSON.parse(response["ram_description"])["free"]);
		    	visits1 = [x1,y1];
		    	visits2 = [x2,y2];
		    	traffic = [
		    	{
		    		Parameter:"IP Address:",Value:response["ip_address"]
		    	},
		    	{
		    		Parameter:"MAC Address",Value:response["mac_address"]
		    	},
		    	{
		    		Parameter:"OS Distribution",Value:response["os_distro"]
		    	},
		    	{
		    		Parameter:"Kernel Version",Value:response["kernel_version"]
		    	},
		    	{
		    		Parameter:"CPU Speed",Value:response["cpu_speed"].toString()+"GHz"
		    	},
		    	{
		    		Parameter:"Last Logged In Time",Value:response["last_active_at"]
		    	},
		    	];
		    }
		});

		


        $("#shieldui-chart2").shieldChart({
            theme: "dark",
            primaryHeader: {
                text: "HardDisk Usage"
            },
            exportOptions: {
                image: false,
                print: false
            },
            dataSeries: [{
                seriesType: "pie",
                collectionAlias: "usage",
                data: visits1
            }]
        });

        $("#shieldui-chart3").shieldChart({
            theme: "dark",
            primaryHeader: {
                text: "RAM Usage"
            },
            exportOptions: {
                image: false,
                print: false
            },
            dataSeries: [{
                seriesType: "pie",
                collectionAlias: "usage",
                data: visits2
            }]
        });

        $("#shieldui-grid1").shieldGrid({
            dataSource: {
                data: traffic
            },
            sorting: {
                multiple: true
            },
            rowHover: false,
            paging: false,
            columns: [
            { field: "Parameter", title: "Parameter" },
            { field: "Value", title: "Value" }
            ]
        }); 
          
	}

	$(document).on("click","#activity",function(){
		window.location = 'activity.html';
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
        console.log(msg+"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6");
        if(msg.indexOf("Alert:")==0)
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

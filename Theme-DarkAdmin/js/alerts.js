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

	function callback(){

		$('#news-list').html("");

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
					$("#news-list").append("<li><i class='fa fa-exclamation-mark fa-4x pull-left'></i><div class='news-item-info'><div class='name'><a href='#'>"+response["results"][i]["text"]+"</a></div><div class='position'></div><div class='time'></div></div></li>");
			    }
			    $("#alerts-drp").append('<li><a href="alerts.html">Go to Alerts</a></li>');
			}
		});
	}

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
        	callback();
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
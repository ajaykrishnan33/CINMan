$(document).ready(function(){

	var host = "192.168.0.102";
	localStorage.setItem("host",host);
	var port = "8000";
	localStorage.setItem("port",port);
	var authToken = "";

	$('#f1').submit(function(e)
	{
	    e.preventDefault();
	    var username=$("#userid").val();
	    var password=$("#pswrd").val();
	    $.post("http://"+host+":"+port+"/api-token-auth/",
	           {"username":username,"password":password}, //use eg. jquery form plugin
	           function(data)
	           {
	           	   authToken = data["token"];
	           	   localStorage.setItem("authToken",authToken);
	           	   localStorage.setItem("username",username);
	               window.location = 'machines.html';
	           }
	    );
	});
});
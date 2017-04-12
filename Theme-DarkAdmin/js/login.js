$(document).ready(function(){

	var host = "localhost";
	var port = "8000";
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
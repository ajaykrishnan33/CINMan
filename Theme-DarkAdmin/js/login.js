$(document).ready(function(){

	var host = "";
	var port = "";
	var authToken = "";
	var flag = false;

	if(localStorage.getItem("host")==null || localStorage.getItem("port")==null)
	{
		$("#hostdiv").show();
		$("#portdiv").show();
		flag=false;
	}
	else
	{
		host = localStorage.getItem("host");
		port = localStorage.getItem("port");
		flag=true;
	}

	$('#f1').submit(function(e)
	{
	    e.preventDefault();
	    var username=$("#userid").val();
	    var password=$("#pswrd").val();
	    if(!flag)
	    {
	    	host = $("#host").val();
	    	port = $("#port").val();
	    }
	    $.post("http://"+host+":"+port+"/api-token-auth/",
	           {"username":username,"password":password}, //use eg. jquery form plugin
	           function(data)
	           {
	           	   authToken = data["token"];
	           	   localStorage.setItem("authToken",authToken);
	           	   localStorage.setItem("username",username);
	           	   if(!flag)
	           	   {
	           	   		localStorage.setItem("host",host);
	   	           	    localStorage.setItem("port",port);
	           	   }
	               window.location = 'machines.html';
	           }
	    );
	});

	$("#cache").click(function(e)
	{
		e.preventDefault();
		localStorage.removeItem("host");
		localStorage.removeItem("port");
	    window.location = 'login.html';
	});
});
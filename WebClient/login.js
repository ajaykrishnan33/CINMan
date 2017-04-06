$(document).ready(function(){

	$("#login").submit(function(){
  /*function to check userid & password*/
      alert("hihh")
      var host="localhost"
	      var port="8000"
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
	    	localStorage.setItem("authToken", response["token"]);
	    	console.log(localStorage.getItem("authToken"));
	    	  	}
	      });
	});
});
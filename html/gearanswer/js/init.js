$(document).ready(function(){
    //create menu
	$(".show-menu").bind("click",function () {  
		$('#'+this.name).toggle();
	});
    $("#core-tabs").tabs(
        { show: { effect: "fadeIn", duration: 800 } }
    );

});


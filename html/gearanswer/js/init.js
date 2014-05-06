
function showUEditor() {
        $("#div-ue").show();
    }
function hideUEditor() {
        $("#div-ue").hide();
    }
function showMDEditor() {
    $("#div-md").show();
    $(".wmd-preview").hide();
}
function hideMDEditor() {
    $("#div-md").hide();
}
function createEditors(){
    $("#editor-md").pagedownBootstrap();
    UE.getEditor('editor-ue');
    if ($.cookie('editor') == "md"){
        hideUEditor();
    }
    else{
         hideMDEditor();
    }
        
}
$(document).ready(function(){
    //create menu
	$(".show-menu").bind("click",function () {  
		$('#'+this.name).toggle();
	});
    $("#core-tabs").tabs(
        { show: { effect: "fadeIn", duration: 800 } }
    );
    
    $( "#use-markdown" ).change(function(){
        hideUEditor();
        showMDEditor();
        $.cookie('editor', 'md');
    });
    $( "#use-ueditor" ).change(function(){
        $.cookie('editor', 'ue');
        hideMDEditor();
        showUEditor();
    });
    
    SyntaxHighlighter.all();
    createEditors();
});


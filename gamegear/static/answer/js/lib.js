
function showUEditor() {
    $.cookie('editor',
         'ue',
         {expires : 10}
        );
    $("#div-ue").show();
}
function hideUEditor() {
    $("#div-ue").hide();
}
function showMDEditor() {
     $.cookie('editor',
         'md',
         {expires : 10}
        );
    $("#div-md").show();
    $(".wmd-preview").hide();
}
function hideMDEditor() {
    $("#div-md").hide();
}
/* Create both of the Editors and hide them
 * depend on the 'editor' value in the cookie.
 * The 'editor' is 'ue' or 'md'.
 * The default editor is markdown editor.
 */
function createEditors(){
    // create editors and display one according to cookie
    $("#editor-md").pagedownBootstrap();
    UE.getEditor('editor-ue');

    if ($.cookie('editor') == "ue"){
        setTimeout(function(){
          $("#use-ueditor").attr('checked','checked');
        },10);
        hideMDEditor();
        showUEditor();
    }
    else{
        setTimeout(function(){
          $("#use-markdown").attr('checked','checked');
        },10);
        hideUEditor();
        showMDEditor();
    } 
    $(".wmd-preview").hide();
        
}
// Rendering all the elements contains md-render class.
function md_render(){
    var converter = new Showdown.converter({ extensions: ['github'] });
    $(".md-render").each(function(){
        text =  converter.makeHtml($(this).html());
        $(this).html(text);
    });
    
}
$(document).ready(function(){
    //create tabs
    $("#core-tabs").tabs(
        { show: { effect: "fadeIn", duration: 800 } }
    );    
});
/*
$(document).ready(function(){
    //create menu
	$(".show-menu").bind("click",function () {  
		$('#'+this.name).toggle();
	});
    //create tabs
    $("#core-tabs").tabs(
        { show: { effect: "fadeIn", duration: 800 } }
    );
    //bind editors change
    $( "#use-markdown" ).change(function(){
        hideUEditor();
        showMDEditor();
        
    });
    $( "#use-ueditor" ).change(function(){
        hideMDEditor();
        showUEditor();
        
    });
    md_render();
    SyntaxHighlighter.all();
    createEditors();
    
    
});
*/

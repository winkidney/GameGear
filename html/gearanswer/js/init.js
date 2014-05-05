
function createUEditor() {
        UE.getEditor('editor-area');
    }
function deleteUEditor() {
        UE.getEditor('editor-area').destroy();
    }
function createMDEditor() {
    $("#editor-area").markdown({
            callback: function(e){
                // Replace selection with some drinks
                $("#use-ueditor").change(e.showEditor())
            }
    });
}
function deleteMDEditor() {
        
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
        deleteUEditor();
        createMDEditor();
    });
    $( "#use-ueditor" ).change(function(){
        deleteMDEditor();
        createUEditor();
    });
    
    SyntaxHighlighter.all();
    createUEditor();
});


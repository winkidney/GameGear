$(document).ready(function(){
    //bind editors change
    $( "#use-markdown" ).change(function(){
        hideUEditor();
        showMDEditor();
        
    });
    $( "#use-ueditor" ).change(function(){
        hideMDEditor();
        showUEditor();
        
    });
    createEditors();
});  

$(document).ready(function(){
    //create menu
	$(".show-menu").bind("click",function () {  
		$('#'+this.name).toggle();
	});
    //jpalyer
    var myOtherOne = new CirclePlayer("#jquery_jplayer_2",
			{   //wav:"file/attack.wav",
                mp3:"file/love.mp3",
                //oga:"http://opengameart.org/sites/default/files/fungi_growth.ogg",
				//m4a:"http://www.jplayer.org/audio/m4a/Miaow-04-Lismore.m4a",
				//oga:"http://www.jplayer.org/audio/ogg/Miaow-04-Lismore.ogg"
			}, {
				cssSelectorAncestor: "#cp_container_2",
                swfPath: "jquery/plugin/jplayer/",
                supplied: "m4a, oga, wav, mp3",
                //solution: "flash, html"
			});

});
//浮动通菜单栏
/*
$.fn.smartFloat = function () {
	var position = function (element) {
		var top = element.offset().top, pos = element.css("position");
		$(window).scroll(function () {
			var scrolls = $(this).scrollTop();
			if (scrolls > 0) {
				if (window.XMLHttpRequest) {
					element.css({ position: "fixed", top: 0 });
				} else {
					element.css({ top: scrolls });
				}
			} else {
				//element.css({position: pos,top: top});        
				element.removeAttr("style");
			}
		});
	};
	return $(this).each(function () {
		position($(this));
	});
};
//绑定
$("#headerSectionFloat").smartFloat();
*/

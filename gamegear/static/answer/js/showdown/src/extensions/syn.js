var syn = function(converter) {
  return [
    // Replace escaped @ symbols
    { type: 'lang', function(text) {
        text = text.replace(/(?:^|\n)```(.*)\n([\s\S]*?)\n```/g,
        function(wholeMatch,m1,m2) {
			var language = m1;
			var codeblock = m2;

			codeblock = _EncodeCode(codeblock);
			codeblock = _Detab(codeblock);
			codeblock = codeblock.replace(/^\n+/g,""); // trim leading newlines
			codeblock = codeblock.replace(/\n+$/g,""); // trim trailing whitespace

			codeblock = "<pre" + (language ? " class=\"" + "brush: "+language + "; toolbar: false;"+'"' : "") + ">" + codeblock + "\n</pre>";

			return hashBlock(codeblock);
		});
    }}
  ];
} 

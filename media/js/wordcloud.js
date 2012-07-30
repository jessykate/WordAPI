$(document).ready(function() {
		// the target width and height are stored in a hidden div with a known id.
		var width = $("#tagcloud_size").width();
		var height = $("#tagcloud_size").height();
		var tgcl = $("#tagcloud");
		// need to specify one of the dimensions as a constraint.
		tgcl.width(width);

		// log the desired cloud dimensions (this is the target)
		console.log("desired wordcloud dimensions");
		console.log( width );
		console.log( height );

		console.log("got here");
		
		// set font size explicitly so we can modify it
		tgcl.css("font-size", "10px");

		// goal is to fit the word sizes to the specified area. check to see if
		// we need to increase or decrease the base font size to meet this
		// goal. 
		var sz = parseInt(tgcl.css("font-size"));
		if (tgcl.height() > height) {
			while ( tgcl.height() > height ) {
				sz = sz - 0.1;
				tgcl.css("font-size", sz);
			} 
		} else {
			while ( tgcl.height() < height ) {
				sz = sz + 0.1;
				tgcl.css("font-size", sz + 1);
				// make sure we don't go *over* the div height
				if (tgcl.height() > height) {
					tgcl.css("font-size", sz - 0.1);
					break;
				}
			} 
		}

		console.log("final wordcloud dimensions:");
		console.log($("#tagcloud").width());
		console.log($("#tagcloud").height());
});

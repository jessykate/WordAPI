(function(){

	num_to_word = function(freq) {
		// takes a number a converts it to a word by converting the integers to
		// words and concatinating them.
		var intwords = {
			'0': 'zero',
			'1': 'one',
			'2': 'two',
			'3': 'three',
			'4': 'four',
			'5': 'five',
			'6': 'six',
			'7': 'seven',
			'8': 'eight',
			'9': 'nine'
		};

		// eg. the string "12"
		var freq_string = freq.toString();
		var words = [];
		for (var idx in freq_string) {
			var word = intwords[freq_string[idx]];
			words.push(word);
		}
		var wordstring = words.join("-");
		return wordstring;
	};

	color_scheme = function(color_a, color_b, total_steps) {
		// expects color_a and color_b to be in hexadecimal RGB format,
		// prefixed by a hash - eg. #FFEEDD

		var default_palette = ["#FF6600", "#CC6626", "#99664D", "#666673", "#336699"];
		
		// if no colours are specified, return a default colour scheme.
		if (!color_a || !color_b) {
			return default_palette;
		}

		// strip the leading hash sign from the color
		color_a = color_a.substr(1, color_a.length-1);
		color_b = color_b.substr(1, color_b.length-1);

		// extract the r, g, and b components of each colour and convert them
		// from hex (base 16) to base 10 
		var ra = parseInt(color_a.substr(0,2), 16);
		var ga = parseInt(color_a.substr(2,4), 16);
		var ba = parseInt(color_a.substr(4,6), 16);
		var rb = parseInt(color_b.substr(0,2), 16);
		var gb = parseInt(color_b.substr(2,4), 16);
		var bb = parseInt(color_b.substr(4,6), 16);

		var delta_r = ra - rb;
		var delta_g = ga - gb;
		var delta_b = ba - bb;

		var steps = parseInt(total_steps) - 1;
		palette = [];
		// note that color_a gets recovered when the value of step == 0
		for (var step in steps) {
			var r = ra - step*(delta_r/steps);
			var g = ga - step*(delta_g/steps);
			var b = ba - step*(delta_b/steps);
			// convert back to hex
			var rgb = '#'+r.toString(16)+g.toString(16)+b.toString(16);
			palette.push(rgb);
		}
		palette.push('#'+color_b);
		return palette;
	};


	wordcloud = function(input, width, height) {
		var tokenizer = /[ \n]/;
		var base_font = "10px";
		var slope = 0.15;
		var normalize_case = true;
		// min_size is in em units. 1em == base font-size. 
		var min_size = 1; 
		var max_words = 100;
		var equn_type = "linear"; // alt: log, exp
		var start_color, end_color, color_steps;
		// stop words list from NLTK 2.0b9
		var stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
			'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
			'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
			'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
			'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
			'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
			'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
			'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
			'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
			'against', 'between', 'into', 'through', 'during', 'before',
			'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
			'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
			'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
			'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
			'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
			'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'];

		// tokenize and determine word counts
		var words = input.split(tokenizer);
		counts = {};
		_.each(words, function(word) {
			word = word.trim();
			if (normalize_case) {
				word = word.toLowerCase();
			}
			if (stop_words.indexOf(word) < 0) {
				if (counts[word]) {
					counts[word] += 1;
				} else {
					counts[word] = 1;
				}
			}
		});

		console.log("counts array");
		console.log(counts);

		// calculate relative sizes. word size are in em (relative to font-size)
		var min_freq = _.min(_.values(counts));
		var b = min_size - slope*min_freq;
		console.log("equation of the line: " + slope.toString() + "x + " + b.toString());
		word_size_em = function(x) {
			var m = slope;
			var intercept = b;
			return m*x + intercept;
		};
		
		// give each wordcloud and wordcloud-tmp space a unique ID in case
		// there are multiple wordclouds on a page. 
		var wordcloud_tmp_id = parseInt(Math.random()*100000).toString();
		var wordcloud_id = parseInt(Math.random()*100000).toString();
		
		// assemble html. each word gets a generic 'word' class as well as a
		// class specific to that frequency. 
		var the_html = "<div class='wordcloud-wrapper' id='" + wordcloud_id + "'> <div class='the-wordcloud'> ";
		_.each(_.keys(counts), function(word) {
			the_html += "<div title='" + counts[word].toString() + "' class='word " + num_to_word(counts[word]) + "'>" + word + "</div> "; 
		});
		// make sure to clear the float, or the the-wordcloud div will have 0
		// dimension.
		the_html += "<div class='clear'></div>";
		the_html += "</div></div>";

		// set the colour scheme
		if (start_color && end_color && color_steps) {
			colors = color_scheme(start_color, end_color, color_steps);
		} else {
			// with no arguments, will return a default colour scheme
			colors = color_scheme();
		}

		// get the distinct count values
		distinct_counts = [];
		for (c in _.values(counts)) {
			if (distinct_counts.indexOf(c) < 0) {
				distinct_counts.push(c);
			}
		}
		
		// assemble the style block
		base_style = "<style type='text/css'>\n";
		base_style += "#"+ wordcloud_id + ", .clear { clear: both; }\n";
		base_style += "#"+ wordcloud_id + ", .word { text-align: center; vertical-align: middle; line-height:1em; padding-right:5px; float:left; }\n";
		for (var idx =0; idx < distinct_counts.length; idx++) {
			// iterate through the available colours
			var color_index = idx % colors.length;
			var color = colors[color_index];
			var count = distinct_counts[idx];
			base_style += "#"+ wordcloud_id + ", ." + num_to_word(count) + "{ font-size: " + word_size_em(count) + "em; color: " + color + "; }\n";
		}
		wc_initial_style = "#"+ wordcloud_id + " .wordcloud-wrapper {font-size: " + base_font + "; width: " + width + "; height: " + height + "; }";
		style_end = "</style>\n";
		style = base_style + wc_initial_style + style_end;
		
		// temporarily inject the html and css in an offscreen div where the font size can
		// be dynamically adjusted. 
		$("body").prepend("<div class='tagcloud-tmp' id='"+ wordcloud_tmp_id +"' style='position: absolute; top:-999px; left:-999px;'></div>");
		$(".tagcloud-tmp").append(style);
		$(".tagcloud-tmp").append(the_html);
		
		// adjust the base font till word cloud takes up maximal area of the
		// div without going over. 
		var target_width = $("#"+wordcloud_id + ", .wordcloud-wrapper").width();
		var target_height = $("#"+wordcloud_id + ", .wordcloud-wrapper").height();
		console.log(target_height);
		console.log(target_width);

		var current_font = parseInt(base_font);
		console.log("the current font size is " + current_font.toString());
		var wc = $("#"+wordcloud_id + ", .the-wordcloud");
		wc.width(target_width);
		if (wc.height() > target_height) {
			while ( wc.height() > target_height ) {
				current_font -= 0.1;
				wc.css("font-size", current_font);
			}
		} else {
			while (wc.height() < target_height ) {
				current_font += 0.1;
				wc.css("font-size", current_font);
				wc.css("font-size", current_font);
				// make sure we don't go *over* the div height
				if (wc.height() > target_height) {
					current_font -= 0.1;
					wc.css("font-size", current_font);
					break;
				}
			}
		}
		
		// update the style block with the calculated font-size, delete the
		// temporary tagcloud, and return the adjusted html and style info. 
		var derived_base_font = current_font;
		//$("#"+wordcloud_tmp_id).remove();
		console.log("the derived font size is " + derived_base_font.toString());
		wc_final_style = "#"+ wordcloud_id + ", .wordcloud-wrapper {font-size: " + derived_base_font + "px; width: " + width + "; height: " + height + "; }";
		style = base_style + wc_final_style + style_end;

		//return style + the_html;

		// place the tagcloud in the document
		//$(div_id).html(the_html);



	};


})( window );

from django.conf import settings
from piston.handler import BaseHandler
from piston.utils import rc
import nltk, urllib, urllib2
import pymongo, pymongo.json_util, pymongo.objectid
import random, math, datetime
from lib import html_unescape, bitly_shorten

try:
    import json
except:
    import simplejson as json

# other things to support: documents, multiple arguments for either
# request or url

# TagCloud by URL
# Diff Function
# PoS Tagging

class GeneralHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    args_required = None
    args_optional = None

    def execute():
        ''' Override this in your child class.'''
        pass

    def read(self, request):
        ''' upon GET requests, retrieves the required and any optional
        arguments, and stores them in self.fargs and self.kwargs,
        respectively. then calls the execute function, which must be
        implemented by the child class and calls the main work
        function of the handler.'''
        print 'in "read"'
        self.fargs = []
        for arg in self.args_required:
            if not request.GET.get(arg, None):
                resp = rc.BAD_REQUEST
                resp.write(': Missing Required Parameter "%s"' % arg)
                return resp
            else:
		thisarg = urllib.unquote_plus(request.GET.get(arg))
                self.fargs.append(thisarg)

        self.kwargs = {}
        for arg in self.args_optional:
            if request.GET.get(arg, None):
		thisarg = urllib.unquote(request.GET.get(arg))
                self.kwargs[arg] = thisarg

	return self.execute()

    def create(self, request):
        ''' mirrors the functionality implemented by read(), for POST
        requests.'''
        print 'in "create"'
        print request.FILES
        self.fargs = []
        for arg in self.args_required:
            if not request.POST.get(arg, None):
                resp = rc.BAD_REQUEST
                resp.write(': Missing Required Parameter "%s"' % arg)
                return resp
            else:
                # assumes only that a single file will be uploaded and it's
                # field name in the form will be 'file'. XXX TODO make this
                # more robust. 
                if arg == 'file':
                    thisarg = request.FILES['file']
                else:
                    thisarg = urllib.unquote_plus(request.POST.get(arg))
                self.fargs.append(thisarg)
        
        self.kwargs = {}
        for arg in self.args_optional:
            if request.POST.get(arg, None):
                thisarg = urllib.unquote(request.POST.get(arg))
                self.kwargs[arg] = thisarg

        return self.execute()


def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'WordAPI/1.0')]
    fp = opener.open(url)
    return fp.read()
    

def tokenize(body, tokenizer=None, strip='true', normalize=True, 
		remove_stopwords = True, custom_stopwords = ''):    

    if strip.lower() != 'false':
        body = nltk.clean_html(body)        
        
	# if tokenizer is None, use a basic tokenizer that takes sequences of
	# alphanumeric characters and includes hyphenated terms.
    if not tokenizer:
        tokenizer = r'[\w\-]+'
    else:
        print 'using custom tokenizer'
        print 'tokenizer: %s' % tokenizer
        tokenizer = urllib.unquote(tokenizer)
    print tokenizer
    try:
        tknizr = nltk.tokenize.RegexpTokenizer(tokenizer)
    except:
        resp = rc.BAD_REQUEST
        resp.write(": Tokenizer parameter must be a valid regular expression.")
        return resp
    #body = body.encode('utf-8')
    tokens = tknizr.tokenize(body)

	# normalize case
    if normalize:
        tokens = [token.lower() for token in tokens] 
    if remove_stopwords:
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords.extend(['1','2','3','4','5','6','7','8','9','0', '-',"'",'"','(',')']) 
		# call lower() on each token because we can't be sure the tokens are
		# normalized. 
        tokens = [token for token in tokens if token.lower() not in stopwords]
	print 'custom_stopwords'
	print custom_stopwords
	if custom_stopwords != '':
		custom = custom_stopwords.split(',')
		custom = [c.strip().lower() for c in custom]
		tokens = [token for token in tokens if token.lower() not in custom]
    return tokens

def _tup_cmp(t1, t2):
    ''' sorts in decreasing order'''
    if t1[1] > t2[1]:
        return -1
    elif t1[1] < t2[1]:
        return 1
    else: return 0

def sort(d):
    items = zip(d.keys(), d.values())
    items.sort(_tup_cmp)
    return items

def num_to_word(freq):
    ''' takes a number a converts it to a word by converting the integers to
    words and concatinating them.'''
    intwords = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
    }

    freq_string = str(freq)
    words = []
    for char in freq_string:
        word = intwords[char]
        words.append(word)
    wordstring = '_'.join(words)
    return wordstring


def color_scheme(color_a=None, color_b=None, total_steps=5):
    '''Has a series of colour schemes to select randomly from, or
       extrapolates between two values to return a custom colour scheme. ''' 
    
    default_palette = ["#FF6600", "#CC6626", "#99664D", "#666673", "#336699"]

    # if no colours are specified, return a random colour scheme. 
    if not color_a or not color_b:
        palette = default_palette

    else:
        steps = int(total_steps)-1

        color_a = color_a.strip('#')
        color_b = color_b.strip('#')

        ra = int(color_a[0:2], 16)
        ga = int(color_a[2:4], 16)
        ba = int(color_a[4:6], 16)
        rb = int(color_b[0:2], 16)
        gb = int(color_b[2:4], 16)
        bb = int(color_b[4:6], 16)

        delta_r = ra - rb
        delta_g = ga - gb
        delta_b = ba - bb

        # note the color_a gets covered by the '0' step. 
        palette = []
        for step in xrange(steps):
            r = ra - step*(delta_r/steps)
            g = ga - step*(delta_g/steps)
            b = ba - step*(delta_b/steps)
            print r,g,b
            rgb = '#'+''.join((hex(r)+hex(g)+hex(b)).split('0x'))
            palette.append(rgb)
        palette.append('#'+color_b)

    return palette

def quadratic_equation(a,b,c):
    a = float(a)
    b = float(b)
    c = float(c)
    x1 = (-b + math.sqrt(pow(b,2.0) - 4.0*a*c))/(2.0*a)
    x2 = (-b - math.sqrt(pow(b,2.0) - 4.0*a*c))/(2.0*a)
    return x1,x2

def fit_to_area(width, height, dist, font):
	pass

def fit_to_area_old(width, height, dist, font):

    w = width
    h = height

    # calculate the number of times a **frequency** occurs
    freqs = {}
    for word, freq in dist:
        freqs[freq] = freqs.get(freq, 0) + 1

    # XX NOT SURE WHY THESE 3 LINES ARE HERE
	# decide the intercept such that the smallest frequency we are visualizing
	# has a 'reasonable' font size-- say, 14px. 
    #min_freq = min([d[1] for d in dist])
    #min_font = 14
    #b = min_font-m*min_freq
    
    # equation of the line: y = mx + b; m=1 so y = x + b
    # where the input x = the frequency of the word, and the output y is the
    # calculated font size. ie, font_size = freq + b. 
    # so w * h = sum over each word (area of the word)
    
    # area of the word is its own width by height. here we assume for
    # simplicity that the font is roughly square (ie a font size of 14px is
    # 14px wide times the number of letters in the word, and 14px high). 

    # so, w * h = (freq + b) = n*(freq+b), where n is the number of times a
    # word with frequency freq appears. 
    
    # to calculate area width * height in px^2:
    # width * height = sum over i: n_i*(f_i + b)^2
    # where we want to solve for b, the intercept of the line.
    # each i'th term simplifies to:
    # nf^2 + 2nfb + nb^2
    # we compute the sum and collect like terms, ending with 
    # a polynomial of the form:
    # a1 + a2*b + a3*b^2 = width*height
    # (a1 - width*height) + a2*b + a3b^2 = 0
    # and then use the quadratic equation to solve for b. 
    a1 = -(w*h)
    a2 = a3 = 0
    m = 1
    print 'calculating coefficients'
    for f, n in freqs.iteritems():
        print f,n
        #a1 += n*pow(f,2.0)
        a1 += n*pow(m,2.0)*pow(f,2.0)
        a2 += 2*n*m*f
        a3 += n

    print 'a1 = %f, a2 = %f, a3 = %f' % (a1,a2,a3)
    # solve for b using quadratic formula
    b1,b2 = quadratic_equation(a1,a2,a3)

    print 'quadratic results'
    print 'b1 = %f, b2 = %f' % (b1, b2)
	# not sure if we want the smaller or bigger solution, but the bigger one
	# will be a translation of the line to the right, resulting in larger fonts
	# for a given frequency. 
    if b1<b2: 
        b = b2
    else: b = b1

    print 'font size determination'
    print "b = %f" % b

    font_size_fn = lambda freq: freq+b
    return font_size_fn

def extrapolate_linear(dist, min_size, slope):
	# explicitly set the indices where the min and max values can be found in
	# the dist list. 
	MAX = 0
	MIN = -1
	# y = mx+b. 
	# m is given by the slope argument
	# min_size occurs when x = min_freq, ie min_size = slope*min_freq + b. 
	# rearrange for b: b = min_size - slope*min_freq
	min_freq = float(dist[MIN][1])
	max_freq = float(dist[MAX][1])
	min_size = float(min_size)

	# if they're all the same frequency, everything is the same size. use the
	# mid-point between max_size and min_size (it's still built as a function 
	# so we can use it easily in place of a dynamic value). 
	if max_freq == min_freq:
		font_size_fn = lambda freq: (max_size + min_size)/2.0
	else:
		m = slope
		b = min_size - m*min_freq
		font_size_fn = lambda freq: m*freq+b

	print 'for the set font size, m was calculated to be %f and b calculated to be %f' % (m, b)
	return font_size_fn

def div_based_layout(divstyle, dist):
	
	body = '''<div %s>''' % (divstyle)
	for word, freq in dist:
		# each word has a class of 'word' in addition to its frequency so that
		# the user may specify additional styling. **note**: make sure the
		# space after the span is maintained; otherwise the spans within the
		# div won't wrap. 
		body += '''<div title="%d" class="word %s">%s</div> ''' % (freq, num_to_word(freq), word)
	body += '''</div>'''
	return body

def svg_based_layout(divstyle, dist):
	body = '''<svg %s><text>''' % (divstyle)
	for word, freq in dist:
		# each word has a class of 'word' in addition to its frequency so that
		# the user may specify additional styling. **note**: make sure the
		# space after the span is maintained; otherwise the spans within the
		# div won't wrap. 
		body += '''<tspan title="%d" class="word %s">%s</tspan> ''' % (freq, num_to_word(freq), word)
	body += '''</text></svg>'''
	return body


def word_cloud(dist, css_id = "", css_class = "", layout = "svg", width=800, 
		height=600, max_words = None, start_color=None, end_color=None, 
		color_steps=None, sort_order="random", equn="linear", slope=0.15, 
		link_prefix=None):

	''' returns a dict with style and body elements. style contains
	defalt styling for the tag cloud, while body contains the html
	markup. '''

	# sort() returns a list of (word, count) tuples in order of decreasing frequency 
	dist = sort(dist) 

	# truncate the list of items if max_words was specified
	if max_words:
		max_words = int(max_words)
		dist = dist[:max_words]            

	# get the number of words remaining in dist (ie the number of tags in the
	# tagcloud) to pass back in the metadata 
	words_in_cloud = len(dist)

	# the equation of the line used here determines the *relative* sizes of
	# different frequency words. actual font sizes are computed with javascript
	# to dynamically fit the words into the specified area. 

	# get the equation of the line AFTER truncating to max_words and BEFORE
	# shuffling the order around.  

	if equn == "log":
		# shifting the logarithm up by 1 gives a word of frequency one size one. 
		font_size_fn = lambda freq: 10*math.log(freq,2) + 1
	elif equn == "exp":  
		font_size_fn = lambda freq: math.pow(freq, 1.2)
	else: # linear
		min_size = 1
		font_size_fn = extrapolate_linear(dist, min_size, slope)

	# determine the sort order. if the sort order is frequency, there's nothing
	# to do since the distribution object is already sorted by frequency. 
	if sort_order == 'random': 
		# shuffles in place
		random.shuffle(dist)
	if sort_order == 'alphabetical':
		dist.sort()

	# assemble the class and id tags for the tag cloud's wrapping div 
	divstyle = '''id="tagcloud"'''
	if css_class != "": 
		divstyle = divstyle[:-1] + " " + class_ + ''' "'''

	# the user can specify a unique id for the tag cloud if they want
	# additional styling applied from their own style sheets. 
	if css_id != "": divstyle += ''' id="%s" ''' % id_
	divstyle = divstyle.strip()	  

	if layout == "svg":
		body = svg_based_layout(divstyle, dist)
	else:
		body = div_based_layout(divstyle, dist)


	if start_color and end_color and color_steps:
		num_colors = int(color_steps)
		colors = color_scheme(start_color, end_color, color_steps)
	else:
		num_colors = 5
		colors = color_scheme()

	# get the distinct frequencies and specify a font-size and color for each,
	# that corresponds to its size 
	freqs = []
	for f in [x[1] for x in dist]: 
		if f not in freqs: freqs.append(f)
	style = '''<style type="text/css">
// important clearfix for divs which wrap floating elements
// see http://nicolasgallagher.com/micro-clearfix-hack/
#hidden-resizer { zoom: 1; }
#hidden-resizer:before, #hidden-resizer:after { content: ""; display: table; }
#hidden-resizer:after { clear: both; }
#tagcloud { font-size: 10px; text-align: center; zoom: 1; }
#tagcloud:before, #tagcloud:after { content: ""; display: table; }
#tagcloud:after { clear: both; }
.word { text-align: center; vertical-align: middle; line-height:1; padding-right:5px; float:left; } '''
	for f in freqs:
		freq_as_word = num_to_word(f)
		color_index = f % num_colors
		color = colors[color_index]
		style += ('''
.%s {font-size: %sem; color: %s }''' 
% (freq_as_word, font_size_fn(f), color))
	style += '''
</style>'''

   # assemble the response (if you get an error on this line, probably mongo is
   # not running)
	oid = pymongo.objectid.ObjectId()
	uid = str(oid)
	long_url = settings.HOME_PAGE + '/cloud/' + uid
	if settings.DEBUG:
		short_url = long_url
	else:
		short_url = bitly_shorten(long_url)
	metadata = {
			'utc_created': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
			'total_tags' : words_in_cloud,        
			'short_url' : short_url,
			}
	record =  {
			'_id': oid, 
			'body': body, 
			'style': style, 
			# hidden div to pass target width and height information onto javascript resizer
			# TODO not all tagclouds will necessarily have width and height?
			'wordcloud_size': '''
<div id="tagcloud_size" style="width:%dpx; height:%dpx; position: absolute; left:-999em;top:-999em;"></div>''' % (width, height),
			'script': '''<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
			<script type="text/javascript" src="/media/js/wordcloud.js"></script>
			''',
			'metadata': metadata
			} 

	print style

	# save to the database
	con = pymongo.Connection()
	collection = con.wordapi.tagclouds
	collection.insert(record)

	return record

class UrlTokenHandler(GeneralHandler):
    allowed_methods = ('GET',)
    args_required = ['url',]
    args_optional = ['tokenizer', 'strip']

    def execute(self):
        return tokenize(self.fargs[0], **self.kwargs )
        
class RequestTokenHandler(GeneralHandler):
    allowed_methods = ('GET', 'POST')
    args_required = ['body']
    args_optional = ['tokenizer', 'strip']
    
    def execute(self):
        return tokenize(self.fargs[0], **self.kwargs )

class UrlFrequencyHandler(GeneralHandler):        
    allowed_methods = ('GET',)
    args_required = ['url']
    args_optional = ['tokenizer', 'strip']

    def execute(self):
        tokens =  tokenize(self.fargs[0], **self.kwargs )
        return nltk.FreqDist(tokens)

class RequestFrequencyHandler(GeneralHandler):        
    allowed_methods = ('GET', 'POST')
    args_required = ['body']
    args_optional = ['tokenizer', 'strip']

    def execute(self):
        tokens =  tokenize(self.fargs[0], **self.kwargs )
        return nltk.FreqDist(tokens)


class CloudRetreiveHandler(BaseHandler):
	''' retrieve an existing tag cloud'''
	allowed_methods = ('GET')
	
	def read(self, request, cloud_id):
		if not cloud_id:
			resp = rc.BAD_REQUEST
			resp.write(': Missing Required Parameter "cloud_id"')
			return resp
		
		print 'retrieved cloud'
		con = pymongo.Connection()
		collection = con.wordapi.tagclouds
		record = collection.find_one({'_id':pymongo.objectid.ObjectId(cloud_id)})
		print record['_id']        
		# pymongo.json_util will properly encode the json-like mongo object
		# return json.dumps(record, default=pymongo.json_util.default)
		return record

class TagCloudBaseHandler(GeneralHandler):
	''' assumes body will be a blob of text, not a url. still has option to
	strip existing html. ''' 
	allowed_methods = ('GET', 'POST')
	# optional args supported by all tag cloud types. required args are
	# specified by the specific child classes. 
	args_optional = ['tokenizer', 'strip', 'max_words', 'normalize', 
		'remove_stopwords', 'sort_order', 'custom_stopwords', 
		# custom color scheme options
		'start_color', 'end_color', 'color_steps',
		# width and height of the div returned
		'width', 'height', 
		# form of the equation from which to extrapolate relative word sizes
		# and scaling factor for linear equation
		'slope', 'equn',
		# user-specified css
		'css_id', 'css_class',
		# custom link prefix
		'link_prefix',
		# layout algorithm (svg or text)
		'layout'
		]

	def execute(self):
		''' default execute method. override for more specific behaviour'''
		tokens = self.get_tokens()
		freq = self.get_freqdist(tokens)
		return self.get_cloud(freq)

	def escape_text(self, raw_text, encoding=None):
		if not encoding:
			encoding = 'utf8'
		#ustring = unicode(raw_text, encoding, 'ignore')
		ustring = html_unescape(raw_text)
		return ustring

	def get_text(self):
		# return the actual contents to be used in the tag cloud. implemented
		# by child class, depending on the call type-- eg. in-line or url
		# reference. 
		pass

	def get_tokens(self):
		tokenizer_opts = {}
		if 'tokenizer' in self.kwargs.keys():
			tokenizer_opts['tokenizer'] = self.kwargs['tokenizer']
		if 'strip' in self.kwargs.keys():
			tokenizer_opts['strip'] = self.kwargs['strip']        
		if 'remove_stopwords' in self.kwargs.keys():
			tokenizer_opts['remove_stopwords'] = self.kwargs['remove_stopwords']        
		if 'normalize' in self.kwargs.keys():
			tokenizer_opts['normalize'] = self.kwargs['normalize']        
		if 'custom_stopwords' in self.kwargs.keys():
			# comma-separated list in string format
			tokenizer_opts['custom_stopwords'] = self.kwargs['custom_stopwords']   
		tokens =  tokenize(self.get_text(), **tokenizer_opts )
		return tokens

	def get_freqdist(self, tokens):
		freq = nltk.FreqDist(tokens)
		return freq

	def get_cloud(self, freq):
		cloud_opts = {}
		if 'width' in self.kwargs.keys():
			cloud_opts['width'] = self.kwargs['width']                
		if 'height' in self.kwargs.keys():
			cloud_opts['height'] = self.kwargs['height']                
		if 'max_words' in self.kwargs.keys():
			cloud_opts['max_words'] = self.kwargs['max_words']                
		if 'start_color' in self.kwargs.keys():
			cloud_opts['start_color'] = self.kwargs['start_color']                
		if 'end_color' in self.kwargs.keys():
			cloud_opts['end_color'] = self.kwargs['end_color']                
		if 'color_steps' in self.kwargs.keys():
			cloud_opts['color_steps'] = self.kwargs['color_steps']                
		if 'sort_order' in self.kwargs.keys():
			cloud_opts['sort_order'] = self.kwargs['sort_order']                
		if 'equn' in self.kwargs.keys():
			cloud_opts['equn'] = self.kwargs['equn']
		if 'slope' in self.kwargs.keys():
			cloud_opts['slope'] = self.kwargs['slope']                
		if 'css_id' in self.kwargs.keys():
			cloud_opts['css_id'] = self.kwargs['css_id']  
		if 'css_class' in self.kwargs.keys():
			cloud_opts['css_class'] = self.kwargs['css_class'] 
		if 'link_prefix' in self.kwargs.keys():
			cloud_opts['link_prefix'] = self.kwargs['link_prefix']    
		if 'layout' in self.kwargs.keys():
			cloud_opts['layout'] = self.kwargs['layout']    

		cloud = word_cloud(freq, **cloud_opts)
		return cloud

class TagCloudBodyHandler(TagCloudBaseHandler):
    # 'body' becomes fargs[0] in the parent class's execute() method
    print 'in body handler'
    args_required = ['body']

    def get_text(self):
        return self.escape_text(self.fargs[0])



class TagCloudFileHandler(TagCloudBaseHandler):
    # 'file' becomes fargs[0] in the parent class's execute() method
    print 'in file handler'
    args_required = ['file']

    def get_text(self):
        fp = self.fargs[0]
        print fp
        # assumes file is small enough to fit into memory..
        tmp_file = ''
        for chunk in fp.chunks():
            tmp_file += chunk
        return self.escape_text(tmp_file)

class TagCloudUrlHandler(TagCloudBaseHandler):
    # 'url' becomes fargs[0] in the parent class's execute() method
    args_required = ['url']

    def get_text(self):
        # the text to be analyzed is passed in via a url, so we need to
        # retrieve it
        url = self.fargs[0]
        if not url.startswith('http://'):
            url = 'http://'+url
        fp = urllib.urlopen(url)
        print 'retrieving text from %s' % url
        raw = fp.read()
        encoding = fp.headers['content-type'].split('charset=')[-1]
        if encoding == 'text/plain':
            encoding = 'ascii'
        elif encoding == 'text/html':
            encoding = 'utf-8'
        ustring = unicode(raw, encoding)
        ustring_escaped = html_unescape(ustring)
        return ustring_escaped


class TagCloudFreqHandler(TagCloudBaseHandler):
    # builds the tag cloud from an already computed frequency distribution
    args_required = ['freqs']
    
    def execute(self):
        freqs = json.loads(self.fargs[0])
        return self.get_cloud(freqs)

# let the user register a call back when something is triggered. 

def keyword_match():
	''' similarity can be computed by asking which other documents share the
	most words with this document (poor man's topic detection) or how
	precisely similar the actual content is, which takes into account word
	order. the former could look at any of: the top x% of words, the top n
	words...''' 
	pass

def diff(doca, docb):
    ''' accepts doca and docb as strings. identifies sections which have been
    added or removed from doca in docb. returns a set of tuples with the
    section and whether it was added or deleted.'''
    
    num_characters = max([len(doca), len(docb)]) 
    for i in num_characters:
        diffs = []
        if doca[i] != docb[i]:
            diffs.append(i)
	pass

def percent_different(doca,docb, unit="words"):
	# unit can be characters, words, sentences, paragraphs. 
	pass

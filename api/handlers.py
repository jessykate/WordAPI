from piston.handler import BaseHandler
from piston.utils import rc
import nltk, urllib, urllib2
import urllib
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
        ''' Override this is your child class.'''
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
		thisarg = urllib.unquote_plus(request.GET.get(arg))
                self.kwargs[arg] = thisarg

        print 'kwargs:'
        print self.kwargs
        # each handler defines an 'execute' function that calls the
        # main work function with arguments stored in the class
        # attributes. might simply call some other function, or can
        # contain the work itself. the former would look something
        # like:
        #
        # def execute(self):
        #     work_func(self.fargs[0], ... self.fargs[n], *self.kwargs)
        # 
	return self.execute()

    def create(self, request):
        ''' mirrors the functionality implemented by read(), for POST
        requests.'''
        print 'in "create"'
        self.fargs = []
        for arg in self.args_required:
            if not request.POST.get(arg, None):
                resp = rc.BAD_REQUEST
                resp.write(': Missing Required Parameter "%s"' % arg)
                return resp
            else:
                thisarg = urllib.unquote_plus(request.POST.get(arg))
                self.fargs.append(thisarg)
        
        self.kwargs = {}
        for arg in self.args_optional:
            if request.POST.get(arg, None):
                thisarg = urllib.unquote_plus(request.POST.get(arg))
                self.kwargs[arg] = thisarg

        # each handler defines an 'execute' function that calls the
        # main work function with arguments stored in the class
        # attributes
        print 'kwargs'
        print self.kwargs
        print ''
        print 'fargs'
        print self.fargs
        return self.execute()


def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'WordAPI/1.0')]
    fp = opener.open(url)
    return fp.read()
    

def tokenize(body, tokenizer=None, strip='true'):    
    if strip.lower() != 'false':
        body = nltk.clean_html(body)        
        
    # if tokenizer is None, use a basic tokenizer that takes sequences of
    # alphanumeric characters and includes hyphenated terms.
    if not tokenizer:
        tokenizer = r'[\w\-]+'
    else:
        # XXX TODO why is this not getting converted to a raw string?
        # convert custom tokenizer to raw string
        tokenizer = r'%s' % str(tokenizer)
    print type(tokenizer)
    try:
        tknizr = nltk.tokenize.RegexpTokenizer(tokenizer)
    except:
        resp = rc.BAD_REQUEST
        resp.write(": Tokenizer parameter must be a valid regular expression.")
        return resp
    tokens = tknizr.tokenize(body)
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


def tag_cloud(dist, id_ = "", class_ = "", width="400", height=None, 
              max_size=20, min_size=10, max_words = None):
    ''' returns a dict with style and body elements. style contains
    defalt styling for the tag cloud, while body contains the html
    markup. '''

    # sort() returns a list of tuples in order of decreasing frequency 
    dist = sort(dist) 
    # explicitly set the indices where the min and max values can be found in
    # the dist list. 
    MAX = 0
    MIN = -1

    # truncate the list of items if max_words was specified
    if max_words:
        dist = dist[:max_words]            
        
    # assemble the class and id tags for the tag cloud's wrapping div 
    divstyle = '''class="tagcloud"'''
    if class_ != "": divstyle = divstyle[:-1] + " " + class_ + ''' "'''
    # the user can specify a unique id for the tag cloud if they want
    # additional styling applied from their own style sheets. 
    if id_ != "": divstyle += ''' id="%s" ''' % id_
    divstyle = divstyle.strip()	  

    body = '''<div %s>''' % divstyle
    for word, freq in dist:
	# each word has a class of 'word' in addition to its frequency so that
	# the user may specify additional styling

    # note: make sure the space after the span is maintained; otherwise the
    # spans within the div won't wrap. 
        body += '''<span class="word %s">%s</span> ''' % (num_to_word(freq),
        word)
    body += '''</div>'''
    #print body

    # get the equation of the line between min_size and max_size:
    # y = mx+b --> max_size = m*max_freq + b, min_size = m*min_freq + b.
    # max_size - min_size = m (max_freq - min_freq) 
    # --> m = (max_size - min_size)/(max_freq - min_freq)
    max_freq = float(dist[MAX][1])
    min_freq = float(dist[MIN][1])
    max_size = float(max_size)
    min_size = float(min_size)
    m = (max_size - min_size)/(max_freq - min_freq)
    print "m = %f" % m
    b = max_size - m*max_freq
    print "b = %f" % b
    size = lambda freq: m*freq+b

    # get the distinct frequencies and specify a font-size for each that
    # corresponds to its size 
    # TODO colours!
    # TODO often each tag is a link to a category list or something else...
    freqs = []
    for f in [x[1] for x in dist]: 
	if f not in freqs: freqs.append(f)
    style = '''<style>
.tagcloud {width: %s; height: %s; text-align: center; }''' % (width, height)
    for f in freqs:
        freq_word = num_to_word(f)
    	style += '''
.%s {padding-left: 15px; padding-right: 15px; font-size: %s; }''' % (freq_word, size(f))
        print f
        print size(f)
    style += '''
</style>'''
    #print 'style portion'
    #print style
  
    return {'body': body, 'style': style}

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

class TagCloudHandler(GeneralHandler):
    ''' assumes body will be a blob of text, not a url. still has option to
	strip existing html. ''' 
    allowed_methods = ('GET', 'POST')
    args_required = ['body']
    args_optional = ['tokenizer', 'strip', 
                     # width and height of the div returned
                     'width', 'height', 
                     # scaling factors for largest and smallest words
                     'max_size', 'min_size']

    def execute(self):
        print 'max_size'
        print self.kwargs
        tokenizer_opts = {}
        if 'tokenizer' in self.kwargs.keys():
            tokenizer_opts['tokenizer'] = self.kwargs['tokenizer']
        if 'strip' in self.kwargs.keys():
            tokenizer_opts['strip'] = self.kwargs['strip']        
        tokens =  tokenize(self.fargs[0], **tokenizer_opts )
        freq = nltk.FreqDist(tokens)

        cloud_opts = {}
        if 'width' in self.kwargs.keys():
            cloud_opts['width'] = self.kwargs['width']                
        if 'height' in self.kwargs.keys():
            cloud_opts['height'] = self.kwargs['height']                
        if 'max_size' in self.kwargs.keys():
            cloud_opts['max_size'] = self.kwargs['max_size']                
        if 'min_size' in self.kwargs.keys():
            cloud_opts['min_size'] = self.kwargs['min_size']                
        cloud = tag_cloud(freq, **cloud_opts)
	return cloud # json.dumps(cloud)

class DiffHandler(GeneralHandler):
	pass

def keyword_match():
	''' similarity can be computed by asking which other documents share the
	most words with this document (poor man's topic detection) or how
	precisely similar the actual content is, which takes into account word
	order. the former could look at any of: the top x% of words, the top n
	words...''' 
	pass

def diff(doca, docb):
	''' identifies sections which have been aded or removed from doca in
	docb. returns a set of tuples with the section and whether it was added
	or deleted.'''
	pass

def percent_different(doca,docb, unit="words"):
	# unit can be characters, words, sentences, paragraphs. 
	pass

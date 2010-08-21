from piston.handler import BaseHandler
from piston.utils import rc
import nltk, urllib, urllib2
import urllib, random
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
		thisarg = urllib.unquote(request.GET.get(arg))
                self.kwargs[arg] = thisarg

        #print 'kwargs:'
        #print self.kwargs
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
                thisarg = urllib.unquote(request.POST.get(arg))
                self.kwargs[arg] = thisarg

        #print 'kwargs'
        #print self.kwargs
        #print ''
        #print 'fargs'
        #print self.fargs

        # each handler defines an 'execute' function that calls the
        # main work function with arguments stored in the class
        # attributes
        return self.execute()


def get_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'WordAPI/1.0')]
    fp = opener.open(url)
    return fp.read()
    

def tokenize(body, tokenizer=None, strip='true', normalize=True, remove_stopwords = True):    
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
    tokens = tknizr.tokenize(body)
    if normalize:
        tokens = [token.lower() for token in tokens] 
    if remove_stopwords:
        stopwords = nltk.corpus.stopwords.words('english')
        # call lower() on each token because we can't be sure the tokens are
        # normalized. 
        tokens = [token for token in tokens if token.lower() not in stopwords]
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

        # the start and end colours are also steps, so subtract 2 from the steps
        # we have to calculate. 
        steps = total_steps - 2

        ra = color_a[0:2]
        ga = color_a[2:4]
        ba = color_a[4:6]
        rb = color_b[0:2]
        gb = color_b[2:4]
        bb = color_b[4:6]

        delta_r = ra - rb
        delta_g = ga - gb
        delta_b = ba - bb

        palette = [color_a,]
        for step in xrange(steps):
            step += 1
            r = ra + step*(delta_r/steps)
            g = ga + step*(delta_g/steps)
            b = ba + step*(delta_b/steps)
            palette.append('#%x%x%x' % (r,g,b))
        palette.append(color_b)

    return palette
         

def tag_cloud(dist, id_ = "", class_ = "", width=None, height=None, 
              max_size=70, min_size=10, max_words = None, sort_order="random"):
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
        max_words = int(max_words)
        dist = dist[:max_words]            

    # get the equation of the line between min_size and max_size. do this AFTER
    # truncating to max_words and BEFORE shuffling the order around.  

    # y = mx+b --> max_size = m*max_freq + b, min_size = m*min_freq + b.
    # max_size - min_size = m (max_freq - min_freq) 
    # --> m = (max_size - min_size)/(max_freq - min_freq)
    max_freq = float(dist[MAX][1])
    min_freq = float(dist[MIN][1])
    max_size = float(max_size)
    min_size = float(min_size)
    # if they're all the same frequency, everything is the same size. use the
    # mid-point between max_size and min_size (it's left as a function so we
    # can use it easily in place of a dynamic value below). 
    if max_freq == min_freq:
        font_size = lambda freq: (max_size + min_size)/2
    else:
        m = (max_size - min_size)/(max_freq - min_freq)
        b = max_size - m*max_freq
        font_size = lambda freq: m*freq+b

    # determine the sort order. if the sort order is frequency, there's nothing
    # to do since the distribution object is already sorted by frequency. 
    if sort_order not in ['random', 'frequency', 'alphabetical']:
        print 'invalid sort orderi; using default = random'
        sort_order = 'random'

    if sort_order == 'random':
        # shuffles in place
        random.shuffle(dist)

    if sort_order == 'alphabetical':
        # not yet implemented 
        pass
    
    # assemble the class and id tags for the tag cloud's wrapping div 
    divstyle = '''class="tagcloud"'''
    if class_ != "": 
        divstyle = divstyle[:-1] + " " + class_ + ''' "'''
    
    # the user can specify a unique id for the tag cloud if they want
    # additional styling applied from their own style sheets. 
    if id_ != "": divstyle += ''' id="%s" ''' % id_
    divstyle = divstyle.strip()	  

    body = '''<div %s>''' % divstyle
    for word, freq in dist:
        # each word has a class of 'word' in addition to its frequency so that
        # the user may specify additional styling. **note**: make sure the
        # space after the span is maintained; otherwise the spans within the
        # div won't wrap. 
        body += '''<span class="word %s">%s</span> ''' % (num_to_word(freq), word)
    body += '''</div>'''
    #print body

    num_colors = 5
    colors = color_scheme(num_colors=num_colors)

    # get the distinct frequencies and specify a font-size and color for each,
    # that corresponds to its size 
    freqs = []
    for f in [x[1] for x in dist]: 
        if f not in freqs: freqs.append(f)
    style = '''<style type="text/css">
.tagcloud {width: %s; height: %s; text-align: center; }
.word { text-align: center; vertical-align: middle; } ''' % (width, height)
    for f in freqs:
        freq_as_word = num_to_word(f)
        color_index = f % num_colors
        color = colors[color_index]
    	style += ('''
.%s {padding-left: 15px; padding-right: 15px; font-size: %s; color: %s }''' 
% (freq_as_word, font_size(f), color))
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

class TagCloudBaseHandler(GeneralHandler):
    ''' assumes body will be a blob of text, not a url. still has option to
	strip existing html. ''' 
    allowed_methods = ('GET', 'POST')
    #args_required = ['body']
    args_optional = ['tokenizer', 'strip', 'max_words', 'normalize', 
                      'remove_stopwords', 'sort_order',
                     # width and height of the div returned
                     'width', 'height', 
                     # scaling factors for largest and smallest words
                     'max_size', 'min_size']

    def get_text(self):
        # return the actual contents to be used in the tag cloud. implemented
        # by child class, depending on the call type-- eg. in-line or url
        # reference. 
        pass

    def execute(self):
        tokenizer_opts = {}
        if 'tokenizer' in self.kwargs.keys():
            tokenizer_opts['tokenizer'] = self.kwargs['tokenizer']
        if 'strip' in self.kwargs.keys():
            tokenizer_opts['strip'] = self.kwargs['strip']        
        if 'remove_stopwords' in self.kwargs.keys():
            tokenizer_opts['remove_stopwords'] = self.kwargs['remove_stopwords']        
        if 'normalize' in self.kwargs.keys():
            tokenizer_opts['normalize'] = self.kwargs['normalize']        
        tokens =  tokenize(self.get_text(), **tokenizer_opts )
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
        if 'max_words' in self.kwargs.keys():
            cloud_opts['max_words'] = self.kwargs['max_words']                
        if 'sort_order' in self.kwargs.keys():
            cloud_opts['sort_order'] = self.kwargs['sort_order']                
            print cloud_opts['sort_order']
        cloud = tag_cloud(freq, **cloud_opts)
	return cloud # json.dumps(cloud)

class TagCloudBodyHandler(TagCloudBaseHandler):
    # 'body' becomes fargs[0] in the parent class's execute() method
    args_required = ['body']

    def get_text(self):
        return self.fargs[0]

class TagCloudUrlHandler(TagCloudBaseHandler):
    # 'url' becomes fargs[0] in the parent class's execute() method
    args_required = ['url']

    def get_text(self):
        # the text to be analyzed is passed in via a url, so we need to retrieve it
        fp = urllib.urlopen(self.fargs[0])
        print 'retrieving text from %s' % self.fargs[0]
        text = fp.read()
        return text

class DiffHandler(GeneralHandler):
	pass


class TopWordComparisonHandler(GeneralHandler):
    ''' takes the top N most frequent words in two documents and says which
    ones are shared between the two.''' 
    pass

class FeedPhraseDetectionHandler(GeneralHandler):
    ''' Lets the user register a url or feed to be checked regularly for a
    specified phrase.''' 
    pass

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

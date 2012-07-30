#!/usr/bin/python

import re, htmlentitydefs
from settings import BITLY_USER, BITLY_KEY
import urllib2, urllib
try:
    import json
except:
    import simplejson as json


def bitly_shorten(long_url):
    # the long_url must contain the protocol
    if not long_url.startswith('http://'):
        long_url = 'http://' + long_url
    base = "http://api.bit.ly/v3/shorten?"
    args = {
        'login': BITLY_USER,
        'apiKey': BITLY_KEY,
        'longUrl' : long_url,
    }
    api_call = base+urllib.urlencode(args)
    fp = urllib2.urlopen(api_call)
    js = json.loads(fp.read())
    return js['data']['url']

def html_unescape(text):
    ''' Function by Fredrik Lundh at
    http://effbot.org/zone/re-sub.htm#unescape-html. Removes HTML or XML
    character references and entities from a text string and returns text, as a
    unicode string as necessary. '''

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

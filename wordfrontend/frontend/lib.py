#!/usr/bin/python

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


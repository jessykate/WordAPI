#!/usr/bin/python

import re, htmlentitydefs

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

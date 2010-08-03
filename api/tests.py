import urllib, urllib2
#from django.conf import settings
try:
    import json
except:
    import simplejson as json


plain_text = '''
A distributed computation consists of a set of processes that cooperate to
achieve a common goal. A main characteristic of these computations is that the
processes do not already share a common global memory and that they communicate
only by exchanging messages over a communication network. Moreover, message
transfer delays are finite yet unpredictable. This computation model defines
what is known as the asynchronous distributed system model, which includes
systems that span large geographic areas and are subject to unpredictable
loads.

A key concept of asynchronous distributed systems is causality. More precisely,
given two events in a distributed computation, a crucial problem is knowing
whether they are causally related. Could the occurrence of one event be a
consequence of the other?

Processes produce message sendings, message receives, and internal events.
Events that are not causally dependent are concurrent. Fidge 1 and Mattern 2
simultaneously and independently introduced vector clocks to let processes
track causality (and concurrency) between the events they produce. A vector
clock is an array of n integers (one entry per process), where the entry j
counts the number of relevant events that process Pj produces. The timestamp of
an event a process produced (or of the local state this event generated) is the
current value of the corresponding process's vector clock. So, by associating
vector timestamps with events or local states, we can safely decide whether two
events or two local states are causally related (see the "A Historical View of
Vector Clocks" sidebar).  '''

html_text = '''
<p class="INTRODUCTION"><span class="dropcap"><font class="INTRODUCTION"
face="Verdana, Arial, Helvetica, sans-serif" size="2">A</font></span> <font
class="INTRODUCTION" face="Verdana, Arial, Helvetica, sans-serif"
size="2">distributed computation consists of a set of processes that cooperate
to achieve a common
goal. A main characteristic of these computations is that the processes do not
already share a common global memory and that they communicate only by
exchanging messages over a communication network. Moreover, message transfer
delays are finite yet unpredictable. This computation model defines what is
known as the <i>asynchronous distributed system model</i>, which includes
systems that span large geographic areas and are subject to unpredictable
loads.</font></p> 
 
<p class="PARAGRAPH"><font face="Verdana, Arial, Helvetica, sans-serif"
size="2">A key concept of asynchronous distributed systems is <i>causality</i>.
More precisely, given two events in a
distributed computation, a crucial problem is knowing whether they are causally
related. Could the occurrence of one event be a consequence of the
other?</font></p> 
 
<p class="PARAGRAPH"><font face="Verdana, Arial, Helvetica, sans-serif"
size="2">Processes produce message sendings, message receives, and internal
events. Events that are not causally
dependent are concurrent. Fidge <a href="#ref1" class="superscript"
target="_blank">1</a> and Mattern <a href="#ref2" class="superscript"
target="_blank">2</a> simultaneously and independently introduced vector clocks
to let processes track causality (and concurrency) between the events they
produce. A vector clock is an array of <i>n</i> integers (one entry per
process), where the entry <i>j</i> counts the number of relevant events that
process <i>P<sub>j</sub></i> produces. The timestamp of an event a process
produced (or of the local state this event generated) is the current value of
the corresponding process's vector clock. So, by associating vector timestamps
with events or local states, we can safely decide whether two events or two
local states are causally related (see the "<a href="#sidebar1"
target="_blank">A Historical View of Vector Clocks</a>"
sidebar).</font></p> 
'''

def test_tagCloud_html():
    data = urllib.urlencode({'body':html_text, 'strip': True})	
    #url = settings.ROOT_URL + "/api/1.0/tagcloud/json"
    url = "http://localhost:8000/api/1.0/tagcloud/json"
    fp = urllib.urlopen(url, data)
    resp = fp.read()
    print resp

def run_tests():
    test_tagCloud_html()

if __name__ == '__main__':
    run_tests()


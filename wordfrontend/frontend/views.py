# Create your views here.
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from frontend.forms import TagCloudForm
import urllib, httplib2
try:
    import json
except:
    import simplejson as json

def render_to_template(request, template, kwargs):
    kwargs.update(csrf(request))
    return render_to_response(template, kwargs)

def Index(request):
    return render_to_response('frontend/index.html')

def tagcloud(request):
    if request.method == 'GET':
        form = TagCloudForm()
        return render_to_template(request, 'frontend/tagcloud.html', {'domain': settings.ROOT_URL,'tagcloud_form' : form })

    else:
        form = TagCloudForm(request.POST)
        # validation function just checks required fields for now, but later should
        # probably validate tokenizer regular expressions etc. 
        if form.is_valid(): 
            data = form.cleaned_data
            args = {}
            for field, value in data.iteritems():
                if value:
                    args[field] = value
            
            if 'body' in args:
                url = settings.ROOT_URL + "/api/1.0/tagcloud/body.json"
            else: # this is a 'url' call
                url = settings.ROOT_URL + "/api/1.0/tagcloud/url.json"

            headers = {'Content-type': 'application/x-www-form-urlencoded'}
            data = urllib.urlencode(args)
            http = httplib2.Http()
            print 'about to make api call to %s' % url
            response, content = http.request(url, 'POST', headers=headers, body=data)
            js = json.loads(content)
            body = js['body']
            style = js['style']
            # note that in the template, body and style need to be given the 'safe'
            # filter so that the markup will be interpreted. otherwise it will be
            # escaped and displayed as strings.
            return render_to_template(request, 'frontend/tagcloud_display.html', {'body' : body,
                                        'style' : style})


        else:
            print request.POST
            print 'Form did not validate'
            form = TagCloudForm(request.POST)
            return render_to_response('frontend/tagcloud.html', 
                                        {'domain': settings.ROOT_URL,
                                        'tagcloud_form' : form
                                        })



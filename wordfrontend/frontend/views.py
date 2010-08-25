# Create your views here.
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from frontend.forms import TagCloudForm
import urllib, httplib2, datetime
import pymongo
from pymongo.objectid import ObjectId
from lib import bitly_shorten
try:
    import json
except:
    import simplejson as json

def render_to_formtemplate(request, template, kwargs):
    ''' Add csrf token, then call the regular render_to_template'''
    kwargs.update(csrf(request))
    return render_to_template(request, template, kwargs)

def render_to_template(request, template, kwargs):
    '''Add standard template variables before rendering the template'''
    kwargs['home_page'] = settings.HOME_PAGE
    return render_to_response(template, kwargs)


def Index(request):
    return render_to_response('frontend/index.html')

def tagcloud(request):
    if request.method == 'GET':
        form = TagCloudForm()
        return render_to_formtemplate(request, 'frontend/tagcloud.html', {'domain': settings.ROOT_URL,'tagcloud_form' : form })

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
            elif 'freqs' in args:
                url = settings.ROOT_URL + "/api/1.0/tagcloud/freq.json"
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

            # replace the full body text with placeholder text, and then pass
            # the API call url to the template so the user can see what was
            # done. 
            control_params = args
            if 'body' in args:
                control_params['body'] = "your text here"
            generator_url = url + '?' + urllib.urlencode(control_params)

            # tell the browser where it can insert a line break
            generator_url_display = generator_url.replace('&', '<wbr>&')

            print type(content)
            # note that in the template, body and style need to be given the 'safe'
            # filter so that the markup will be interpreted. otherwise it will be
            # escaped and displayed as strings.
            return render_to_formtemplate(request, 'frontend/tagcloud_display.html', {'body' : body,
                                        'style' : style, 'generator_url' : generator_url,
                                        'generator_url_display': generator_url_display, 
                                        'tagcloud_json': content})


        else:
            print request.POST
            print 'Form did not validate'
            form = TagCloudForm(request.POST)
            return render_to_response('frontend/tagcloud.html', 
                                        {'domain': settings.ROOT_URL,
                                        'tagcloud_form' : form
                                        })

def save(request):
    if request.method == 'GET':
        return HttpResponseRedirect("/")

    # save data and url to db
    data = request.POST.get('data')
    record = json.loads(data)
    record['created'] = datetime.datetime.now()
    record['update_type'] = request.POST.get('update')
    if request.POST.get('name', None):
        record['cloud_name'] = request.POST.get('name')
    # record['owner'] = username
    # record['permissions'] = public
    
    # create the unique id for this record
    oid = ObjectId()
    uid = str(oid)
    record['_id'] = oid
    # create short link
    long_url = settings.HOME_PAGE + '/cloud/' + uid
    short_url = bitly_shorten(long_url)
    print short_url
    record['short_url'] = short_url
    con = pymongo.Connection()
    collection = con.wordapi.tagclouds
    collection.insert(record)

    # redirect to the cloud's page
    return HttpResponseRedirect("/cloud/%s" % uid)

    # a dynamic tagcloud saves the source information and rendering preferences

def cloud(request, cloud_id):
    print 'cloud id to be looked up: ', cloud_id
    con = pymongo.Connection()
    collection = con.wordapi.tagclouds
    record = collection.find_one({'_id':ObjectId(cloud_id)})
    return render_to_template(request, 'frontend/cloud.html', {'cloud':record})


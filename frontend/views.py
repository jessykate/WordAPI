# Create your views here.
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from frontend.forms import TagCloudForm, NewTopicForm
import urllib, httplib2, datetime, re
import pymongo
import pymongo
from pymongo.objectid import ObjectId
try:
    import json
except:
    import simplejson as json

def render_to_formtemplate(request, template, kwargs={}):
    ''' Add csrf token, then call the regular render_to_template'''
    kwargs.update(csrf(request))
    return render_to_template(request, template, kwargs)

def render_to_template(request, template, kwargs={}):
    # calls the RequestContext which populates with default template variables
    return render_to_response(template, kwargs, 
                context_instance=RequestContext(request))



def new_document(request):
    if request.method == 'GET':
        form = TagCloudForm()
        return render_to_formtemplate(request, 'frontend/newdoc.html', 
                {'domain': settings.API_URL,'tagcloud_form' : form })

    else:
        form = TagCloudForm(request.POST, request.FILES)
        print request.FILES
        # validation function just checks required fields for now, but later should
        # probably validate tokenizer regular expressions etc. 
        if form.is_valid(): 
            data = form.cleaned_data
            args = {}
            for field, value in data.iteritems():
                if value:
                    args[field] = value
            
            if 'file' in args:
                url = settings.API_URL + "/api/1.0/tagcloud/file.json"
                fp = request.FILES['file']
                tmp_file = ''
                for chunk in fp.chunks():
                    tmp_file += chunk 
                args['file'] = tmp_file

            elif 'body' in args:
                url = settings.API_URL + "/api/1.0/tagcloud/body.json"
                #  normalize the character encoding on any input text
                args['body'] = args['body'].encode('ascii', 'replace')

            elif 'freqs' in args:
                url = settings.API_URL + "/api/1.0/tagcloud/freq.json"
            else: # this is a 'url' call
                url = settings.API_URL + "/api/1.0/tagcloud/url.json"

            # XXX this is a temporary hack until we get the ajax-y resize
            # working. set the max_words and div size to something reasonable. 
            args['max_words'] = 100
            
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                        'enctype': 'enctype="multipart/form-data"'}
            data = urllib.urlencode(args)
            http = httplib2.Http()
            print 'about to make api call to %s' % url
            #print url + '?' + data
            response, content = http.request(url, 'POST', headers=headers, body=data)
            try:
                js = json.loads(content)
                body = js['body']
                style = js['style']
                metadata = js['metadata']
                cloud_id = js['_id']
            except:
                return HttpResponse('<b>API Error</b><br><br>'+content)
                return

            return HttpResponseRedirect("/cloud/%s" % cloud_id)
        else:
            print request.POST
            print 'Form did not validate'
            form = TagCloudForm(request.POST)
            return render_to_formtemplate(request, 'frontend/newdoc.html', 
                                        {'domain': settings.API_URL,
                                        'tagcloud_form' : form
                                        })

def cloud(request, cloud_id):

    print cloud_id
    if re.search('[^0-9a-zA-Z]', cloud_id):
        return HttpResponse('Invalid Cloud ID')

    url = settings.API_URL + '/api/1.0/cloud/' + cloud_id + '.json'
    print 'retrieving cloud...'
    print url
    http = httplib2.Http()
    response, content = http.request(url, 'GET')
    try:
        record = json.loads(content)
    except:
        return HttpResponse('<b>API Error</b><br><br>'+content)

    # XXX TODO this needs to be its own form, not the tag cloud form. 
    form = TagCloudForm()

    #generator_url = url + '?' + urllib.urlencode(control_params)
    # tell the browser where it can insert a line break
    #generator_url_display = generator_url.replace('&', '<wbr>&')

     # note that in the template, body and style need to be given the 'safe'
    # filter so that the markup will be interpreted. otherwise it will be
    # escaped and displayed as strings.
    return render_to_template(request, 'frontend/cloud.html', {'cloud':record, 'update_form':form})

def new_topic(request):
    #topic_form = NewTopicForm(request.POST)
    if request.method == 'POST':
        # get the fields and construct a form to match
        form_data = request.POST
        print form_data
        topic_form = topic_form_generator(form_data)
        return render_to_formtemplate(request, 'frontend/newtopic.html', {'topic_form': topic_form})
        # ---> compute stats --> redirect to topic homepage<br>
    else:
        return render_to_formtemplate(request, 'frontend/newtopic.html')

def topic_form_generator(form_data):
    file_sources = 0
    web_sources = 0
    for k,v in form_data.iteritems():
        if 'web_source' in k:
            web_sources += 1
        elif 'file_source' in k:
            file_sources += 1
    return NewTopicForm(form_data, file_sources=file_sources, 
            web_sources=web_sources)


def topic(request, topic_id):
    # if !saved:
    #   message: this topic has not yet been saved! click here to save
    #vocab, wordcloud, graph of frequency<br>
    #add a classifier<br>
    pass

#def new_document(request):
#    pass

def new_collection(request):
    pass


#def save(request):
#    if request.method == 'GET':
#        return HttpResponseRedirect("/")
#
#    # save data and url to db
#    data = request.POST.get('data')
#    record = json.loads(data)
#    record['created'] = datetime.datetime.now()
#    record['update_type'] = request.POST.get('update')
#    if request.POST.get('name', None):
#        record['cloud_name'] = request.POST.get('name')
#    # record['owner'] = username
#    # record['permissions'] = public
#    
#    # create the unique id for this record
#    oid = ObjectId()
#    uid = str(oid)
#    record['_id'] = oid
#    # create short link
#    long_url = settings.HOME_PAGE + '/cloud/' + uid
#    short_url = bitly_shorten(long_url)
#    print short_url
#    record['short_url'] = short_url
#    con = pymongo.Connection()
#    collection = con.wordapi.tagclouds
#    collection.insert(record)
#
#    # redirect to the cloud's page
#    return HttpResponseRedirect("/cloud/%s" % uid)
#
#    # a dynamic tagcloud saves the source information and rendering preferences



from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from frontend.views import *

urlpatterns = patterns('',
    url(r'^learn', direct_to_template, {'template': 'frontend/learn.html'}),
    url(r'^create', direct_to_template, {'template': 'frontend/create.html'}),
    url(r'^examples', direct_to_template, {'template': 'frontend/examples.html'}),
    url(r'^browse', direct_to_template, {'template': 'frontend/browse.html'}),
    # need the trailing $ after api since the api calls start with /api too
    url(r'^api$', direct_to_template, {'template': 'frontend/api.html'}),

    url(r'^cloud/(?P<cloud_id>\w+)', cloud),
    url(r'^topic/new$', new_topic),
    url(r'^document/new$', new_document),
    url(r'^collecion/new$', new_collection),
#  url(r'^login'),
    url(r'^$',  direct_to_template, {'template': 'frontend/index.html'}),

)

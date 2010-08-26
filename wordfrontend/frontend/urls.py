from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from wordfrontend.frontend.views import *

urlpatterns = patterns('',
  url(r'^tagcloud$', tagcloud),
  url(r'^cloud/(?P<cloud_id>\w+)', cloud),
  url(r'^save$', save),
  url(r'^learn', direct_to_template, {'template': 'frontend/learn.html'}),
  url(r'^create', direct_to_template, {'template': 'frontend/create.html'}),
  url(r'^examples', direct_to_template, {'template': 'frontend/examples.html'}),
  url(r'^browse', direct_to_template, {'template': 'frontend/browse.html'}),
  url(r'^api', direct_to_template, {'template': 'frontend/api.html'}),
#  url(r'^login'),
  url(r'^$',  direct_to_template, {'template': 'frontend/index.html'}),

)

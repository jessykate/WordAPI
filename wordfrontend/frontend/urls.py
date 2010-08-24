from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from wordfrontend.frontend.views import *

urlpatterns = patterns('',
  url(r'^tagcloud$', tagcloud),
  url(r'^cloud/(?P<cloud_id>\w+)', cloud),
  url(r'^save$', save),
  url(r'^$', Index),

)

from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from wordfrontend.frontend.views import *

urlpatterns = patterns('',
  url(r'^tagcloud$', tagcloud),
  url(r'^save', save),
  url(r'^$', Index),

)

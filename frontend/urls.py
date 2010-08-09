from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from wordapi.frontend.views import *

urlpatterns = patterns('',
  url(r'^tagcloud$', tagcloud),
  url(r'^$', Index),

)

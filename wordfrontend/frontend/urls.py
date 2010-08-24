from django.conf.urls.defaults import patterns, url
from wordfrontend.frontend.views import *

urlpatterns = patterns('',
  url(r'^tagcloud$', tagcloud),
  url(r'^$', Index),

)

from wordapi.api.handlers import (
    UrlTokenHandler, RequestTokenHandler, 
    UrlFrequencyHandler, RequestFrequencyHandler,
    TagCloudBodyHandler, TagCloudUrlHandler,
    TagCloudFreqHandler,TagCloudFileHandler,
    CloudRetreiveHandler,
    )

from django.conf.urls.defaults import patterns, url
from piston.resource import Resource

urlpatterns = patterns('',
  # tokenize the contents of the url passed in the request                       
  url(r'^tokenize/url\.(?P<emitter_format>.+)$', Resource(UrlTokenHandler)),
  # tokenize the contents of the content passed in the request
  url(r'^tokenize/request\.(?P<emitter_format>.+)$', Resource(RequestTokenHandler)),
  # calculate the token frequency of the contents at the url passed in                       
  url(r'^frequency/url\.(?P<emitter_format>.+)$', Resource(UrlFrequencyHandler)),
  # calculate the token frequency of the contents passed in                       
  url(r'^frequency/request\.(?P<emitter_format>.+)$', Resource(RequestFrequencyHandler)),
  # build a tag cloud from the contents passed in 
  url(r'^tagcloud/body\.(?P<emitter_format>.+)$', Resource(TagCloudBodyHandler)),
  # build a tag cloud from the url passed in 
  url(r'^tagcloud/url\.(?P<emitter_format>.+)$', Resource(TagCloudUrlHandler)),
  # build a tag cloud from the json-encoded dictionary of frequencies passed in 
  url(r'^tagcloud/freq\.(?P<emitter_format>.+)$', Resource(TagCloudFreqHandler)),
  # retreive a tag cloud
  url(r'^cloud/(?P<cloud_id>[0-9A-Za-z]+)\.(?P<emitter_format>.+)$', Resource(CloudRetreiveHandler)),
  # build a tag cloud from the file uploaded
  url(r'^tagcloud/file\.(?P<emitter_format>.+)$', Resource(TagCloudFileHandler)),

)

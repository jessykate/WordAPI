from django.db import models

# Create your models here.

''' 
Some algorithms build a statistical model of a single topic. What are the most
frequent/high entropy words in this set of documents? A single topic model can
be used to form a classifier 

supervised/unsupervised --> topic models --> classifiers / results
'''

# classifier methods take a document and return the most similar topic, by the
# method specified.
    
def kmeans():
    pass

def lda():
    pass

def cosine_similarity():
    pass

def tfidf_similarity():
    pass

def difference():
    pass

def entropy():
    pass


class Scheduler(object):
    '''Scheduler lets you manage when and how source documents are retrieved
    to update a model or classifier. You might want to gather docs once an hour
    for 3 days, or every Monday indefinitely, or every night at midnight.
    Schedules can be registered with any model, topic or classifier type. '''
    pass

class DocumentSet(object):
    ''' A document set is used to build a set of topic models from one or more
    source documents.'''
    pass 

class Topic(object):
    sources = []
    created = None
    last_updated = None
    update = None #static, manual, auto
    model = None # tfidf, regular freq, k-means...
    public = False

class Source(object):
    uri = None
    created = None
    updated = None

'''
Created on Sep 25, 2015

@author: anilkatta
'''

from django.conf.urls import patterns, url
from views import DocumentView
from views import DocumentDetailView
from views import PropertiesList
from django.conf import settings

urlpatterns = patterns('fileupload.views',
    #url(r'^upload_form_serializer/$', 'upload_form_serializer'),
    url(r'^upload_form_serializer/$', DocumentView.as_view()),
    url(r'^documentdetails/$', DocumentDetailView.as_view()),
    url(r'^propkeylist/$', PropertiesList.as_view()),
)
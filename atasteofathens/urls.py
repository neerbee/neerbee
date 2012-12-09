from django.conf.urls import patterns, include, url
from coffin.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'spots.views.index'),
    url(r'^spots/', include('spots.urls')),
    url(r'^accounts/', include('accounts.urls')),
)

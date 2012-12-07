from django.conf.urls import patterns, include, url
from coffin.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'atasteofathens.spots.views.index'),
    url(r'^spots/', include('atasteofathens.spots.urls')),
    url(r'^accounts/', include('atasteofathens.accounts.urls')),
#    url(r'^admin/', include('atasteofathens.admin.urls')),
)

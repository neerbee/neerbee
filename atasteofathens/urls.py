from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^mongonaut/', include('mongonaut.urls')),
    url(r'^spots/', include('atasteofathens.spots.urls')),
    url(r'^accounts/', include('atasteofathens.accounts.urls')),
    url(r'^$', 'atasteofathens.spots.views.index'),
#    url(r'^admin/', include('atasteofathens.admin.urls')),
)

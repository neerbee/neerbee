from django.conf.urls import patterns, include, url

#spot_resource = SpotResource()

urlpatterns = patterns('',
    url(r'^$', 'neerbee.spots.views.index'),
    url(r'^spots/', include('neerbee.spots.urls', namespace="spots")),
    url(r'^accounts/', include('neerbee.accounts.urls')),
    url(r'^accounts/', include('neerbee.registration.urls')),
)

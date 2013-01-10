from django.conf.urls import patterns, include, url

urlpatterns = patterns(
        'neerbee.spots.views',
        url(r'^$', 'spots', name="spots"),
        url(r'^edit/(?P<spot_slug>\S+)/$', 'new_spot', name="new_spot"),
        url(r'^new/$', 'new_spot', name="new_spot"),
        url(r'^(?P<spot_slug>\S+)/$', 'spot_profile', name="spot_profile"),
)

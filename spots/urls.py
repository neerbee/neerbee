from django.conf.urls import patterns, include, url
from spots.api import SpotResource

spot_resource = SpotResource()

urlpatterns = patterns(
        'spots.views',
        url(r'^api/', include(spot_resource.urls)),
        url(r'^$', 'spots', name="spots"),
        url(r'^users/$', 'users'),
        #url(r'^user/(?P<user_name>\S+)/rate/$', 'user_rate'),
        url(r'^user/(?P<user_name>\S+)/$', 'user_profile'),
        url(r'^(?P<spot_slug>\S+)/$', 'spot_profile', name="spot_profile"),
)

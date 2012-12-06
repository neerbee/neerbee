from django.conf.urls import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns(
        'atasteofathens.spots.views',
        url(r'^$', 'spots'),
        url(r'^users/$', 'users'),
        #url(r'^user/(?P<user_name>\S+)/rate/$', 'user_rate'),
        #url(r'^user/(?P<user_name>\S+)/$', 'user_profile'),
        #url(r'^spot/(?P<spot_slug>\S+)/$', 'spot_profile'),
        url(r'^spots/$', 'spots'),
)

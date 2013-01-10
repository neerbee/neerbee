from django.conf.urls import patterns, include, url

urlpatterns = patterns(
        'neerbee.spots.views',
        url(r'^$', 'spots', name="spots"),
        url(r'^edit/(?P<spot_slug>\S+)/$', 'create_or_edit_spot', name="edit_spot"),
        url(r'^new/$', 'create_or_edit_spot', name="create_spot"),
        url(r'^(?P<spot_slug>\S+)/$', 'spot_profile', name="spot_profile"),
)

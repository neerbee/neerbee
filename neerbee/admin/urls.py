from django.conf.urls import patterns, include, url

urlpatterns = patterns(
        'neerbee.spot.views',
        url(r'^edit_spot/(?P<spot_slug>\S+)/$', 'create_or_edit_spot', name="edit_spot"),
        url(r'^create_spot/$', 'create_or_edit_spot', name="create_spot"),
)
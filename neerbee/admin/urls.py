from django.conf.urls import patterns, include, url

urlpatterns = patterns(
        '',
        url(r'^edit_spot/(?P<spot_slug>\S+)/$', 'neerbee.spots.views.create_or_edit_spot', name="edit_spot"),
        url(r'^create_spot/$', 'neerbee.spots.views.create_or_edit_spot', name="create_spot"),
)
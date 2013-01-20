from django.conf.urls import patterns, include, url

from spots.views import SpotCreateView, SpotUpdateView

urlpatterns = patterns(
        '',
        url(
            regex=r'^edit_spot/(?P<spot_slug>\S+)/$',
            view=SpotUpdateView.as_view(),
            name="edit_spot"
        ),
        url(
            regex=r'^create_spot/$',
            view=SpotCreateView.as_view(),
            name="create_spot"
        ),
)

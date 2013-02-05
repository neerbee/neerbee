from django.conf.urls import patterns, include, url

from .views import SpotDetailView, SpotListView, SpotCreateView, SpotLikenessView

urlpatterns = patterns(
        'spots.views',
        url(
            regex=r'^$',
            view=SpotListView.as_view(),
            name="spots"
        ),
        url(
            regex=r'^athens/(?P<spot_slug>\S+)/$',
            view=SpotDetailView.as_view(), 
            name="spot_profile"
        ),
)

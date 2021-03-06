from django.conf.urls import patterns, include, url

from spots.views import SpotCreateView, SpotUpdateView

from .views import AdminPanelView, UserListView

urlpatterns = patterns(
        '',
        url(
            regex=r'^$',
            view=AdminPanelView.as_view(),
            name="admin_panel"
        ),
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
        url(
            regex=r'^user_list/$',
            view=UserListView.as_view(),
            name="user_list"
        ),
)

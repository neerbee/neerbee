from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from tastypie.api import Api

from neerbee.api import *
from users.views import UserHomeView, UserSettingsView
from spots.views import SpotLikenessView, SpotTraitView

v1_api = Api(api_name='v1')
v1_api.register(SpotResource())
v1_api.register(ServiceResource())
v1_api.register(ServiceFoodResource())
v1_api.register(ServiceBarResource())
v1_api.register(ServiceCoffeeResource())
v1_api.register(ServiceClubResource())

urlpatterns = patterns('',
    url(
    	regex=r'^$',
    	view=UserHomeView.as_view(),
    	name="user_home"
    ),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include('admin.urls', namespace="admin")),
    url(
        regex=r'^api/v1/spot/(?P<spot_slug>\S+)/likeness/',
        view=SpotLikenessView.as_view(),
        name="spot_likeness"
    ),
    url(
        regex=r'^api/v1/spot/(?P<spot_slug>\S+)/trait/',
        view=SpotTraitView.as_view(),
        name="spot_trait"
    ),
    url(r'^api/', include(v1_api.urls)),
    url(
    	regex=r'^settings/',
    	view=UserSettingsView.as_view(),
        name="user_settings"
    ),
    url(r'^spots/', include('spots.urls', namespace="spots")),
)

urlpatterns += patterns('',  
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.staging.STATIC_ROOT}),  
)  
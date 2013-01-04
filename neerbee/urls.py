from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from api.resources import *

v1_api = Api(api_name='v1')
v1_api.register(SpotResource())
v1_api.register(ServiceResource())
v1_api.register(ServiceFoodResource())
v1_api.register(ServiceBarResource())
v1_api.register(ServiceCoffeeResource())
v1_api.register(ServiceClubResource())

urlpatterns = patterns('',
    url(r'^$', 'neerbee.users.views.user_home'),
    url(r'^accounts/', include('neerbee.accounts.urls')),
    url(r'^accounts/', include('neerbee.registration.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^settings/', 'neerbee.users.views.user_settings',
        name="user_settings"),
    url(r'^spots/', include('neerbee.spots.urls', namespace="spots")),
)

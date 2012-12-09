from tastypie import authorization
from tastypie_mongoengine import resources
from spots.models import *

class SpotResource(resources.MongoEngineResource):
    class Meta:
        queryset = Spot.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'spot'

class ServiceFoodResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceFood

class ServiceBarResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceBar

class ServiceCoffeeResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceCoffee

class ServiceClubResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceClub

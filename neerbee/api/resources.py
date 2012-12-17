from tastypie import authorization
from tastypie_mongoengine import fields, resources
from neerbee.spots.models import *


class ServiceFoodResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceFood
        resource_name = 'servicefood'

class ServiceBarResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceBar
        resource_name = 'servicebar'

class ServiceCoffeeResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceCoffee
        resource_name = 'servicecoffee'

class ServiceClubResource(resources.MongoEngineResource):
    class Meta:
        object_class = ServiceClub
        resource_name = 'serviceclub'

class ServiceResource(resources.MongoEngineResource):
    class Meta:
        object_class = Service
        allowed_methods = ('get')
        authorization = authorization.Authorization()

        polymorphic = {
                'serviceFood': ServiceFoodResource,
                'serviceBar': ServiceBarResource,
                'serviceCoffee': ServiceCoffeeResource,
                'serviceClub': ServiceClubResource
        }

class SpotResource(resources.MongoEngineResource):
    services = fields.EmbeddedListField(
                    of='neerbee.api.resources.ServiceResource', 
                    attribute='services', 
                    full=True, 
                    null=True
                    ) 
    class Meta:
        queryset = Spot.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'spot'


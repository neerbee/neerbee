from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie import authorization
from tastypie import authentication
from tastypie.utils import trailing_slash
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
        #authorization = authorization.Authorization()

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
        authentication = authentication.BasicAuthentication() 
        authorization = authorization.DjangoAuthorization()
        resource_name = 'spot'

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = Spot.objects(name__contains=request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        models = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            models.append(bundle)

        object_list = {
                'models': models,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


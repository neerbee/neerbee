from mongoengine import *
from django.template.defaultfilters import slugify
from neerbee.users.models import Bee

class Service(EmbeddedDocument):
    service_type = StringField(max_length=50, required=True)

    def __unicode__(self):
        return self.service_type

class ServiceFood(Service):
    category = StringField(max_length=100, required=True)
    delivery = BooleanField()
    take_out = BooleanField()
    # hours

    def __unicode__(self):
        return "Food"

class ServiceBar(Service):
    category = StringField(max_length=100, required=True)
    # hours

    def __unicode__(self):
        return "Bar"

class ServiceCoffee(Service):
    board_games = BooleanField()   
    # hours

    def __unicode__(self):
        return "Coffee"

class ServiceClub(Service):
    coat_check = BooleanField()
    face_control = BooleanField()
    # hours

    def __unicode__(self):
        return "Club"


class Spot(Document):
    name = StringField(max_length=200, required=True)
    address = StringField(max_length=200, required=True)
    neighbourhood = StringField(max_length=200, required=True)
    phone = StringField(max_length=20)
    website = StringField(max_length=200)
    location = GeoPointField()
    SERVICE_CHOICES = (
            ServiceFood,
            ServiceBar,
            ServiceCoffee,
            ServiceClub,
    )
    services = ListField(
                    EmbeddedDocumentField(Service)
               )
    PRICE_RANGES = (
            (1, '$'),
            (2, '$$'),
            (3, '$$$'),
            (4, '$$$$'),
            (5, '$$$$$'),
    )
    price = IntField(choices=PRICE_RANGES)
    wi_fi = BooleanField()
    credit_card = BooleanField()
    wheelchair = BooleanField()
    tv = BooleanField()
    smoking = BooleanField()
    self_service = BooleanField()
    reservations = BooleanField()
    snacks = BooleanField()
    outdoor_seating = BooleanField()
    parking = BooleanField()

    author = ReferenceField(Bee)

    slug = StringField(max_length=255, required=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.name)[:50]
            return super(Spot, self).save(*args, **kwargs)


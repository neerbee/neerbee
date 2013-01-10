from mongoengine import *
from neerbee.tools import unique_slugify

class Service(EmbeddedDocument):
    service_type = StringField(max_length=50, required=True)

    def __unicode__(self):
        return self.service_type

class ServiceFood(Service):
    service_type = "Food"
    category = StringField(max_length=100, required=True)
    delivery = BooleanField()
    take_out = BooleanField()
    # hours

    def __unicode__(self):
        return "Food"

class ServiceBar(Service):
    service_type = "Bar"
    category = StringField(max_length=100, required=True)
    # hours
    
    def __unicode__(self):
        return "Bar"

class ServiceCoffee(Service):
    service_type = "Coffee"
    board_games = BooleanField()   
    # hours

    def __unicode__(self):
        return "Coffee"

class ServiceClub(Service):
    service_type = "Club"
    coat_check = BooleanField()
    face_control = BooleanField()
    # hours

    def __unicode__(self):
        return "Club"


class Spot(Document):
    name = StringField(max_length=200, required=True)
    address = StringField(max_length=200, required=True)
    neighbourhood = StringField(max_length=200, required=True)
    pobox = StringField(max_length=20)
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
    price = IntField()
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

    slug = StringField(max_length=255, required=True, unique=True)

    meta = {
        'indexes': ['name']
    }

    def __unicode__(self):
        if self.slug:
            return self.slug
        else:
            return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            unique_slugify(self, self.name)
        return super(Spot, self).save(*args, **kwargs)

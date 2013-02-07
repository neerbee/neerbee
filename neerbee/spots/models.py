from django.core.urlresolvers import reverse

from mongoengine import *

from .tools import unique_slugify
from .el_en_transliterate import only_latin_chars, transliterate_text


class ServiceHours(EmbeddedDocument):
    # 0-6 where 0 is Monday
    weekday = IntField(required=True)
    starting = IntField()
    ending = IntField()

    def __unicode__(self):
        return self.day + " " + str(self.starting) + "-" + str(self.ending)


class Service(EmbeddedDocument):
    service_type = StringField(max_length=50, required=True)
    offered_days = ListField(
                        EmbeddedDocumentField(ServiceHours)
                    )

    def __unicode__(self):
        return self.service_type

    def is_offered_on_day(self, day):
        for offered_day in self.offered_days:
            if offered_day.weekday == day:
                return True
        return False

    def is_offered_on_daytime(self, day, hour, minute):
        time_check = hour * 100 + minute
        for offered_day in self.offered_days:
            if offered_day.weekday == day and offered_day.starting <= time_check <= offered_day.ending:
                return True
        return False


class ServiceFood(Service):
    service_type = "Food"
    category = StringField(max_length=100, required=True)
    delivery = BooleanField()
    take_out = BooleanField()

    def __unicode__(self):
        return "Food"


class ServiceBar(Service):
    service_type = "Bar"
    category = StringField(max_length=100, required=True)
    
    def __unicode__(self):
        return "Bar"


class ServiceCoffee(Service):
    service_type = "Coffee"
    board_games = BooleanField()   

    def __unicode__(self):
        return "Coffee"


class ServiceClub(Service):
    service_type = "Club"
    coat_check = BooleanField()
    face_control = BooleanField()

    def __unicode__(self):
        return "Club"


class Spot(Document):
    name = StringField(max_length=200, required=True)
    city = StringField(max_length=20, required=True)
    address = StringField(max_length=200, required=True)
    neighbourhood = StringField(max_length=200, required=True)
    pobox = StringField(max_length=20)
    phone = StringField(max_length=20)
    website = StringField(max_length=200)
    location = GeoPointField()
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
        'indexes': ['name', 'slug']
    }

    def __unicode__(self):
        if self.slug:
            return self.slug
        else:
            return self.name

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        name = self.name
        neighbourhood = self.neighbourhood
        if not self.slug:
            if not only_latin_chars(self.name):
                name = transliterate_text(self.name)
            if not only_latin_chars(self.neighbourhood):
                neighbourhood = transliterate_text(self.neighbourhood)

            unique_slugify(self, name + "-" + neighbourhood)
        return super(Spot, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('spots:spot_profile', args=[self.slug])

    def get_services(self):
        return {service.service_type for service in self.services}

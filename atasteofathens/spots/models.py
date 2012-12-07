from mongoengine import *

class ServiceFood(EmbeddedDocument):
    category = StringField(max_length=100)
    delivery = BooleanField()
    take_out = BooleanField()

class ServiceBar(EmbeddedDocument):
    # happyhour?
    best_nights = ListField(StringField(max_length=50))
    good_for_dancing = BooleanField()

#class ServiceCoffee(EmbeddedDocument):

#class ServiceClub(EmbeddedDocument):

class Spot(Document):
    name = StringField(max_length=200, required=True)
    address = StringField(max_length=200)
    neighbourhood = StringField(max_length=200)
    phone = StringField(max_length=20)
    website = StringField(max_length=200)
    location = GeoPointField()
    SERVICE_CHOICES = (
            ServiceFood,
            ServiceBar,
            # ServiceCoffee,
            # ServiceClub,
    )
    services = ListField(
                    GenericEmbeddedDocumentField(
                        choices=SERVICE_CHOICES
                    )
               )
    PRICE_RANGES = (
            (1, '$'),
            (2, '$$'),
            (3, '$$$'),
            (4, '$$$$'),
            (5, '$$$$$'),
    )
    price = IntField(choices=PRICE_RANGES)
    music = ListField(StringField(max_length=50))
    wi_fi = BooleanField()
    credit_card = BooleanField()
    wheelchair = BooleanField()
    tv = BooleanField()
    smoking = BooleanField()
    NOISE_RANGES = (
            (1, 'low'),
            (2, 'average'),
            (3, 'high'),
    )
    noise_level = IntField(choices=NOISE_RANGES)
    ATTIRE_RANGES = (
            (1, 'casual'),
            (2, 'smart'),
            (3, 'formal'),
    )
    attire = IntField(choices=ATTIRE_RANGES)
    waiter_service = BooleanField()
    live_music = BooleanField()
    group_friendly = BooleanField()
    date_friendly = BooleanField()
    reservations = BooleanField()
    face_control = BooleanField()

    slug = StringField(max_length=255, required=True)
    

    ## alcohol?
    ## hours?
    def __unicode__(self):
        return self.name

"""
class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='r_ratings')
    user = models.ForeignKey(AuthUser, related_name='u_ratings')
    RATING_RANGES = (
            (0, 'bad'),
            (1, 'OK'),
            (2, 'good'),
    )
    rating_value = models.PositiveSmallIntegerField('Rating', choices=RATING_RANGES)
    #rating_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + " has rated '" + self.restaurant.name + "'"
"""

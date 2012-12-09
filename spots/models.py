from mongoengine import *

class ServiceFood(EmbeddedDocument):
    category = StringField(max_length=100)
    delivery = BooleanField()
    take_out = BooleanField()
    # hours

class ServiceBar(EmbeddedDocument):
    category = StringField(max_length=100)
    # hours

class ServiceCoffee(EmbeddedDocument):
    board_games = BooleanField()   
    # hours

class ServiceClub(EmbeddedDocument):
    coat_check = BooleanField()
    face_control = BooleanField()
    # hours

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
            ServiceCoffee,
            ServiceClub,
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

    slug = StringField(max_length=255, required=True)

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

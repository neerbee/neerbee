from mongoengine import *
from mongoengine.django.auth import User
from neerbee.spots.models import Spot

class Bee(User):
    likes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    dislikes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))

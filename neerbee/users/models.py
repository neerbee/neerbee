# Custom neerbee user, extends mongoengine user.
from mongoengine.django.auth import User
from mongoengine import *

class Bee(User):
    age = IntField()

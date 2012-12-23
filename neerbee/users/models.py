from mongoengine import *
from mongoengine.django.auth import User

class Bee(User):
    age = IntField()

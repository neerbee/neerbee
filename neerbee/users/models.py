import datetime

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from mongoengine import *
from mongoengine.django.auth import User

from spots.models import Spot
from spots.traits import Traits

@receiver(user_logged_in)
def get_preferred_language(sender, **kwargs):
	if kwargs['user'].preferred_language:
		lang_code = kwargs['user'].preferred_language
		kwargs['request'].session['django_language'] = lang_code


class Bee(User):
    likes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    dislikes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    preferred_language = StringField(max_length=10)

    def likes_spot(self, spot):
        return spot in self.likes

    def dislikes_spot(self, spot):
        return spot in self.dislikes

    def remove_like(self, spot):
        if spot in self.likes:
            self.likes.remove(spot)
            return True
        else:
            return False

    def remove_dislike(self, spot):
        if spot in self.dislikes:
            self.dislikes.remove(spot)
            return True
        else:
            return False


class Like(Document):
    user = ReferenceField(Bee)
    spot = ReferenceField(Spot)

    def __unicode__(self):
        return "Like"


class Dislike(Document):
    user = ReferenceField(Bee)
    spot = ReferenceField(Spot)



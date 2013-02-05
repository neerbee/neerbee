import datetime

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from mongoengine import *
from mongoengine.django.auth import User

from spots.models import Spot

@receiver(user_logged_in)
def get_preferred_language(sender, **kwargs):
	if kwargs['user'].preferred_language:
		lang_code = kwargs['user'].preferred_language
		kwargs['request'].session['django_language'] = lang_code

class Like(EmbeddedDocument):
    spot = ReferenceField(Spot)
    liked_at = DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return self.spot.name


class Dislike(EmbeddedDocument):
    spot = ReferenceField(Spot)
    disliked_at = DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return self.spot.name   

class Bee(User):
    likes = ListField(EmbeddedDocumentField(Like))
    dislikes = ListField(EmbeddedDocumentField(Dislike))
    preferred_language = StringField(max_length=10)

    def likes_spot(self, spot):
        return spot in (like.spot for like in self.likes)

    def dislikes_spot(self, spot):
        return spot in (dislike.spot for dislike in self.dislikes)    

    def get_like(self, spot):
        if self.likes_spot(spot):
            return [like for like in self.likes if spot == like.spot][0]
        else:
            return None

    def get_dislike(self, spot):
        if self.dislikes_spot(spot):
            return [dislike for dislike in self.dislikes if spot == dislike.spot][0]
        else:
            return None

    def remove_like(self, spot):
        like = self.get_like(spot)
        if like:
            self.likes.remove(like)   
            return True
        else:
            return False

    def remove_dislike(self, spot):
        dislike = self.get_dislike(spot)
        if dislike:
            self.dislikes.remove(dislike)
            return True
        else:
            return False
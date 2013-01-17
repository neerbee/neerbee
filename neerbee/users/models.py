from mongoengine import *
from mongoengine.django.auth import User
from neerbee.spots.models import Spot
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def get_preferred_language(sender, **kwargs):
	request = kwargs['request']
	user = kwargs['user']
	if user.preferred_language:
		request.session['django_language'] = user.preferred_language
	else:
		request.session['django_language'] = 'el'

class Bee(User):
    likes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    dislikes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    preferred_language = StringField(max_length=10, default='en')

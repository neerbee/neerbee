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


class SpotTraits(EmbeddedDocument):
    spot = ReferenceField(Spot)
    traits = ListField(StringField(max_length=50))


class Bee(User):
    likes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    dislikes = ListField(ReferenceField(Spot, reverse_delete_rule=CASCADE))
    spot_traits = ListField(
                        EmbeddedDocumentField(SpotTraits)
                    )
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

    def has_added_traits_in_spot(self, spot):
        for spot_trait in self.spot_traits:
            if spot_trait.spot == spot:
                return True
        return False

    def get_spot_traits(self, spot):
        for spot_trait in self.spot_traits:
            if spot_trait.spot == spot:
                return spot_trait.traits
        return None

    def add_trait_to_spot(self, spot, trait):
        traits = self.get_spot_traits(spot)
        if traits and trait not in traits:
            traits.append(trait)
        else:
            spot_trait = SpotTraits(spot=spot, traits=[])
            spot_trait.traits.append(trait)
            self.spot_traits.append(spot_trait)



class Like(Document):
    user = ReferenceField(Bee)
    spot = ReferenceField(Spot)


class Dislike(Document):
    user = ReferenceField(Bee)
    spot = ReferenceField(Spot)


class Trait(Document):
    user = ReferenceField(Bee)
    spot = ReferenceField(Spot)
    trait = StringField(max_length=50)
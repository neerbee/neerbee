from django import forms
from django.forms.widgets import HiddenInput

from .models import Spot, ServiceFood, ServiceBar, ServiceCoffee, ServiceClub

class SpotForm(forms.Form):
    # general spot attributes
    name = forms.CharField(max_length=200, label="Name")
    address = forms.CharField(max_length=200, label="Address")
    neighbourhood = forms.CharField(max_length=200, label="Neighbourhood")
    pobox = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20, required=False)
    website = forms.CharField(max_length=200, required=False)
    # location
    PRICE_RANGES = (
            ('', ''),
            (1, '$'),
            (2, '$$'),
            (3, '$$$'),
            (4, '$$$$'),
            (5, '$$$$$'),
    )
    price = forms.ChoiceField(choices=PRICE_RANGES, required=False)
    wi_fi = forms.BooleanField(required=False)
    credit_card = forms.BooleanField(required=False)
    wheelchair = forms.BooleanField(required=False)
    tv = forms.BooleanField(required=False)
    smoking = forms.BooleanField(required=False)
    self_service = forms.BooleanField(required=False)
    reservations = forms.BooleanField(required=False)
    snacks = forms.BooleanField(required=False)
    outdoor_seating = forms.BooleanField(required=False)
    parking = forms.BooleanField(required=False)

    longtitude = forms.CharField(max_length=100, widget=HiddenInput, label="Longtitude", required=False)
    latitude = forms.CharField(max_length=100, widget=HiddenInput, label="Latitude", required=False)

    # service-specific spot attributes
    service_food = forms.BooleanField(required=False)
    service_bar = forms.BooleanField(required=False)
    service_coffee = forms.BooleanField(required=False)
    service_club = forms.BooleanField(required=False)
    
    # FOOD
    food_category = forms.CharField(max_length=100, required=False)
    food_delivery = forms.BooleanField(required=False)
    food_take_out = forms.BooleanField(required=False)

    # BAR
    bar_category = forms.CharField(max_length=100, required=False)

    # COFFEE
    coffee_board_games = forms.BooleanField(required=False)

    # CLUB
    club_coat_check = forms.BooleanField(required=False)
    club_face_control = forms.BooleanField(required=False)

    def clean(self):
        # perform service-specific validation
        cleaned_data = super(SpotForm, self).clean()
        service_food = cleaned_data.get("service_food")
        service_bar = cleaned_data.get("service_bar")
        service_coffee = cleaned_data.get("service_coffee")
        service_club = cleaned_data.get("service_club")
        food_category = cleaned_data.get("food_category")
        bar_category = cleaned_data.get("bar_category")

        if not (service_food or service_bar or service_coffee or service_club):
            msg = u"Spot must offer at least one service."
            raise forms.ValidationError(msg)
        elif service_food and not food_category:
            msg = u"Must specify food category."
            raise forms.ValidationError(msg)
        elif service_bar and not bar_category:
            msg = u"Must specify bar category."
            raise forms.ValidationError(msg)

        return cleaned_data

    def save(self, spot):
        spot.services = []
        if self.cleaned_data.get('service_food'):
            service_food = ServiceFood(category =
                                        self.cleaned_data['food_category'])
            if self.cleaned_data.get('food_delivery'):
                service_food.delivery = self.cleaned_data['food_delivery']
            if self.cleaned_data.get('food_take_out'):
                service_food.take_out = self.cleaned_data['food_take_out']

            spot.services.append(service_food)

        if self.cleaned_data.get('service_bar'):
            service_bar = ServiceBar(category =
                                        self.cleaned_data['bar_category'])

            spot.services.append(service_bar)

        if self.cleaned_data.get('service_coffee'):
            service_coffee = ServiceCoffee()
            if self.cleaned_data.get('coffee_board_games'):
                service_coffee.board_games = self.cleaned_data[
                                                'coffee_board_games']
            
            spot.services.append(service_coffee)

        if self.cleaned_data.get('service_club'):
            service_club = ServiceClub()
            if self.cleaned_data.get('club_coat_check'):
                service_club.coat_check = self.cleaned_data[
                                                'club_coat_check']
            if self.cleaned_data.get('club_face_control'):
                service_club.face_control = self.cleaned_data[
                                                'club_face_control']

            spot.services.append(service_club)

        # store location    
        if self.cleaned_data.get('latitude') and self.cleaned_data.get('longtitude'):
            spot.location = [float(self.cleaned_data['longtitude']), float(self.cleaned_data['latitude'])]    


        # add any existing details
        if self.cleaned_data.get('phone'):
            spot.phone = self.cleaned_data['phone']
        if self.cleaned_data.get('website'):
            spot.website = self.cleaned_data['website']
        if self.cleaned_data.get('price'):
            spot.price = self.cleaned_data['price']
        if self.cleaned_data.get('wi_fi'):
            spot.wi_fi = self.cleaned_data['wi_fi']
        if self.cleaned_data.get('credit_card'):
            spot.credit_card = self.cleaned_data['credit_card']
        if self.cleaned_data.get('wheelchair'):
            spot.wheelchair = self.cleaned_data['wheelchair']
        if self.cleaned_data.get('tv'):
            spot.tv = self.cleaned_data['tv']
        if self.cleaned_data.get('smoking'):
            spot.smoking = self.cleaned_data['smoking']
        if self.cleaned_data.get('self_service'):
            spot.self_service = self.cleaned_data['self_service']
        if self.cleaned_data.get('reservations'):
            spot.reservations = self.cleaned_data['reservations']
        if self.cleaned_data.get('snacks'):
            spot.snacks = self.cleaned_data['snacks']
        if self.cleaned_data.get('outdoor_seating'):
            spot.outdoor_seating = self.cleaned_data['outdoor_seating']
        if self.cleaned_data.get('parking'):
            spot.parking = self.cleaned_data['parking']

        # finally, save spot in database
        spot.save()
                                        


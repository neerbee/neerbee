from django import forms

class SpotForm(forms.Form):
    # general spot attributes
    name = forms.CharField(max_length=200, label="Name")
    address = forms.CharField(max_length=200, label="Address")
    neighbourhood = forms.CharField(max_length=200, label="Neighbourhood")
    phone = forms.CharField(max_length=20, required=False)
    website = forms.CharField(max_length=200, required=False)
    # location
    PRICE_RANGES = (
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


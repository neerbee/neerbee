from django.shortcuts import render
from django.http import HttpResponseRedirect
from mongoengine.django.shortcuts import get_document_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from models import *
from forms import SpotForm

def spots(request):
    spot_list = Spot.objects.all()
    return render(request, 'spots/spot_list.html', {'item_list': spot_list})

def spot_profile(request, spot_slug):
    s = get_document_or_404(Spot, slug=spot_slug)
    
    return render(request, 'spots/spot_profile.html', {'spot': s})

# called by admin app
@login_required
def create_or_edit_spot(request, spot_slug=None):
    if request.method == 'POST':
        form = SpotForm(request.POST)
        if form.is_valid():
            # create new Spot object first only with mandatory fields
            if 'delete' in request.POST:
                s = get_document_or_404(Spot, slug=spot_slug)
                s.delete()
                return HttpResponseRedirect('/spots/') # Redirect after POST

            if spot_slug is None:
                new_spot = Spot(name = form.cleaned_data['name'],
                            address = form.cleaned_data['address'],
                            neighbourhood = form.cleaned_data['neighbourhood'],
                            pobox = form.cleaned_data['pobox'])
            else:
                # this is an edit form
                new_spot = get_document_or_404(Spot, slug=spot_slug)
                # should be able to even change spot name but must solve
                # slug issues first
                #if form.cleaned_data.get('name'):
                #    new_spot.name = form.cleaned_data['name']
                if form.cleaned_data.get('address'):
                    new_spot.address = form.cleaned_data['address']
                #if form.cleaned_data.get('neighbourhood'):
                #    new_spot.neighbourhood = form.cleaned_data['neighbourhood']
                if form.cleaned_data.get('pobox'):
                    new_spot.pobox = form.cleaned_data['pobox']    

            # create service list
            new_spot.services = []
            if form.cleaned_data.get('service_food'):
                service_food = ServiceFood(category = 
                                            form.cleaned_data['food_category'])
                if form.cleaned_data.get('food_delivery'):
                    service_food.delivery = form.cleaned_data['food_delivery']
                if form.cleaned_data.get('food_take_out'):
                    service_food.take_out = form.cleaned_data['food_take_out']

                new_spot.services.append(service_food)

            if form.cleaned_data.get('service_bar'):
                service_bar = ServiceBar(category = 
                                            form.cleaned_data['bar_category'])

                new_spot.services.append(service_bar)

            if form.cleaned_data.get('service_coffee'):
                service_coffee = ServiceCoffee()
                if form.cleaned_data.get('coffee_board_games'):
                    service_coffee.board_games = form.cleaned_data[
                                                'coffee_board_games']

                new_spot.services.append(service_coffee)

            if form.cleaned_data.get('service_club'):
                service_club = ServiceClub()
                if form.cleaned_data.get('club_coat_check'):
                    service_club.coat_check =form.cleaned_data[
                                                'club_coat_check']
                if form.cleaned_data.get('club_face_control'):
                    service_club.face_control =form.cleaned_data[
                                                'club_face_control']

                new_spot.services.append(service_club)

            # add any existing details
            if form.cleaned_data.get('phone'):
                new_spot.phone = form.cleaned_data['phone']
            if form.cleaned_data.get('website'):
                new_spot.website = form.cleaned_data['website']
            if form.cleaned_data.get('price'):
                new_spot.price = form.cleaned_data['price']
            if form.cleaned_data.get('wi_fi'):
                new_spot.wi_fi = form.cleaned_data['wi_fi']
            if form.cleaned_data.get('credit_card'):
                new_spot.credit_card = form.cleaned_data['credit_card']
            if form.cleaned_data.get('wheelchair'):
                new_spot.wheelchair = form.cleaned_data['wheelchair']
            if form.cleaned_data.get('tv'):
                new_spot.tv = form.cleaned_data['tv']
            if form.cleaned_data.get('smoking'):
                new_spot.smoking = form.cleaned_data['smoking']
            if form.cleaned_data.get('self_service'):
                new_spot.self_service = form.cleaned_data['self_service']
            if form.cleaned_data.get('reservations'):
                new_spot.reservations = form.cleaned_data['reservations']
            if form.cleaned_data.get('snacks'):
                new_spot.snacks = form.cleaned_data['snacks']
            if form.cleaned_data.get('outdoor_seating'):
                new_spot.outdoor_seating = form.cleaned_data['outdoor_seating']
            if form.cleaned_data.get('parking'):
                new_spot.parking = form.cleaned_data['parking']

            # finally, save spot in database
            new_spot.save()
            return HttpResponseRedirect('/spots/') # Redirect after POST
    else:
        if spot_slug is None:
            form = SpotForm() # An unbound form
        else:
            # this is an edit form
            s = get_document_or_404(Spot, slug=spot_slug)

            # take care of service-specific information
            for service in s._data['services']:
                if service.__class__ is ServiceFood:
                    s._data['service_food'] = True
                    s._data['food_category'] = service.category
                    s._data['food_delivery'] = service.delivery
                    s._data['food_take_out'] = service.take_out
                elif service.__class__ is ServiceBar:
                    s._data['service_bar'] = True
                    s._data['bar_category'] = service.category
                elif service.__class__ is ServiceCoffee:
                    s._data['service_coffee'] = True
                    s._data['coffee_board_games'] = service.board_games
                elif service.__class__ is ServiceClub:
                    s._data['service_club'] = True
                    s._data['club_coat_check'] = service.coat_check
                    s._data['club_face_control'] = service.face_control

            form = SpotForm(initial=s._data)


    return render(request, 'spots/create_or_edit_spot.html', {
        'form': form,
        'spot_slug': spot_slug,
    })

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _

from mongoengine.django.shortcuts import get_document_or_404
from braces.views import LoginRequiredMixin

from users.views import IsStaffMixin
from .models import *
from .forms import SpotForm


class SpotListView(TemplateView):
    template_name = "spots/spot_list.html"
    
    def get_context_data(self, **kwargs):
        spot_list = Spot.objects.order_by('name')
        return {'item_list': spot_list}


class SpotDetailView(TemplateView):
    template_name = "spots/spot_profile.html"

    def get(self, request, *args, **kwargs):
        spot = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        likes = False
        for like in request.user.likes:
            if spot == like.spot:
                likes = True

        dislikes = False
        for dislike in request.user.dislikes:
            if spot == dislike.spot:
                dislikes = True
     
        return render(request, self.template_name, {
                                    'spot': spot,
                                    'likes': likes,
                                    'dislikes': dislikes,
                                    })


class SpotCreateView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = "spots/create_or_edit_spot.html"

    def get(self, request, *args, **kwargs):
        form = SpotForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SpotForm(request.POST)

        if form.is_valid():
            new_spot = Spot(name = form.cleaned_data['name'],
                            city = form.cleaned_data['city'],
                            address = form.cleaned_data['address'],
                            neighbourhood = form.cleaned_data['neighbourhood'],
                            pobox = form.cleaned_data['pobox'])

            form.save(new_spot)
            msg = _("Spot created!")
            messages.success(request, msg)
            return HttpResponseRedirect('/spots/') # Redirect after POST 

           
class SpotUpdateView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = "spots/create_or_edit_spot.html"

    def get(self, request, *args, **kwargs):
        spot_slug = kwargs['spot_slug']
        s = get_document_or_404(Spot, slug=spot_slug)
        # take care of service-specific information
        # in the future I think it should be taken care of
        # in the form, not in the view. maybe override constructor
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

        if s._data.get('location'):
            s._data['longtitude'] = s._data['location'][0]
            s._data['latitude'] = s._data['location'][1]

        form = SpotForm(initial=s._data)

        return render(request, self.template_name, {
                                            'form': form,
                                            'spot_slug': spot_slug
                                            })

    def post(self, request, *args, **kwargs):
        form = SpotForm(request.POST)
        spot_slug = kwargs['spot_slug']
        # check if POST was to delete spot
        if 'delete' in request.POST:
            s = get_document_or_404(Spot, slug=spot_slug)
            s.delete()
            msg = _("Spot deleted!")
            messages.success(request, msg)
            return HttpResponseRedirect('/spots/')
        # then POST was to edit spot
        if form.is_valid():
            new_spot = get_document_or_404(Spot, slug=spot_slug)
            form.save(new_spot)
            msg = _("Spot updated!")
            messages.success(request, msg)
            return HttpResponseRedirect('/spots/') # Redirect after POST 

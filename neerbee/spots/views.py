from operator import itemgetter
from random import randint

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import TemplateView, View
from django.utils.translation import ugettext as _

from mongoengine.django.shortcuts import get_document_or_404
from braces.views import LoginRequiredMixin, JSONResponseMixin

from users.views import IsStaffMixin
from users.models import Like, Dislike, Trait
from .models import *
from .forms import SpotForm
from .traits import get_service_traits, get_non_service_traits


class SpotListView(LoginRequiredMixin, TemplateView):
    template_name = "spots/spot_list.html"
    
    def get_context_data(self, **kwargs):
        spot_list = Spot.objects.order_by('name')
        return {'item_list': spot_list}


class SpotDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spots/spot_profile.html"

    def get(self, request, *args, **kwargs):
        spot = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        
        likes = request.user.likes_spot(spot)
        dislikes = request.user.dislikes_spot(spot)
     
        return render(request, self.template_name, {
                                    'spot': spot,
                                    'likes': likes,
                                    'dislikes': dislikes,
                                    })


class SpotLikenessView(LoginRequiredMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        spot = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        
        if request.POST.get('action') == 'like' and not request.user.likes_spot(spot):
            if request.user.dislikes_spot(spot):
                Dislike.objects(user=request.user, spot=spot).first().delete()
                request.user.remove_dislike(spot)
            request.user.likes.append(spot)
            request.user.save()
            Like(user=request.user, spot=spot).save()
            return self.render_json_response({'action': 'like'})
        elif request.POST.get('action') == 'dislike' and not request.user.dislikes_spot(spot):
            if request.user.likes_spot(spot):
                Like.objects(user=request.user, spot=spot).first().delete()
                request.user.remove_like(spot)
            request.user.dislikes.append(spot)
            request.user.save()
            Dislike(user=request.user, spot=spot).save()
            return self.render_json_response({'action': 'dislike'})
        elif request.POST.get('action') == 'neutral':
            if request.user.likes_spot(spot):
                Like.objects(user=request.user, spot=spot).first().delete()
                request.user.remove_like(spot)   
            else:
                Dislike.objects(user=request.user, spot=spot).first().delete()
                request.user.remove_dislike(spot)

            request.user.save()
            return self.render_json_response({'action': 'neutral'})

        raise Http404


class SpotTraitView(LoginRequiredMixin, JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        #return self.render_json_response({trait:1 for trait in traits})
        spot = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        traits = set()
        for service in spot.get_services():
            traits = traits | get_service_traits(service)

        traits = traits | get_non_service_traits()
        # remove traits that user has voted for
        traits = traits - set(request.user.get_spot_traits(spot))
        #trait_list = sorted([{"text":trait, "weight":randint(1,10)} for trait in traits], key=itemgetter('weight'), reverse=True)
        trait_list = [{"text":trait, "weight":randint(1,10)} for trait in traits]
        if request.GET.get('number'):
            trait_list = trait_list[:int(request.GET.get('number'))]
        return self.render_json_response(trait_list)

    def post(self, request, *args, **kwargs):
        spot = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        traits = set()
        for service in spot.get_services():
            traits = traits | get_service_traits(service)

        traits = traits | get_non_service_traits()
        trait = request.POST.get('trait')
        if trait in traits:
            Trait(user=request.user, spot=spot, trait=trait).save()
            request.user.add_trait_to_spot(spot, trait)
            request.user.save()
            return self.render_json_response({'trait': trait})

        raise Http404


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

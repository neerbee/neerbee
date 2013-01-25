from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView

from mongoengine.django.shortcuts import get_document_or_404
from braces.views import LoginRequiredMixin

from .models import *
from .forms import SpotForm


class SpotListView(TemplateView):
    template_name = "spots/spot_list.html"
    
    def get_context_data(self, **kwargs):
        spot_list = Spot.objects.all()
        return {'item_list': spot_list}


class SpotDetailView(TemplateView):
    template_name = "spots/spot_profile.html"

    def get_context_data(self, **kwargs):
        s = get_document_or_404(Spot, slug=kwargs['spot_slug'])
        return {'spot': s}


class SpotCreateView(LoginRequiredMixin, TemplateView):
    template_name = "spots/create_or_edit_spot.html"

    def get(self, request, *args, **kwargs):
        form = SpotForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SpotForm(request.POST)

        if form.is_valid():
            new_spot = Spot(name = form.cleaned_data['name'],
                            address = form.cleaned_data['address'],
                            neighbourhood = form.cleaned_data['neighbourhood'],
                            pobox = form.cleaned_data['pobox'])

            form.save(new_spot)
            msg = 'Spot created!'
            messages.info(request, msg)
            return HttpResponseRedirect('/spots/') # Redirect after POST 

           
class SpotUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "spots/create_or_edit_spot.html"

    def get(self, request, *args, **kwargs):
        spot_slug = kwargs['spot_slug']
        spot = get_document_or_404(Spot, slug=spot_slug)

        form = SpotForm(spot)

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
            msg = 'Spot deleted!'
            messages.info(request, msg)
            return HttpResponseRedirect('/spots/')
        # then POST was to edit spot
        if form.is_valid():
            new_spot = get_document_or_404(Spot, slug=spot_slug)
            # should be able to change name and neighbourhood but
            # must solve slug issues first
            if form.cleaned_data.get('address'):
                new_spot.address = form.cleaned_data['address']
            if form.cleaned_data.get('pobox'):
                new_spot.pobox = form.cleaned_data['pobox']

            form.save(new_spot)
            msg = 'Spot updated!'
            messages.info(request, msg)
            return HttpResponseRedirect('/spots/') # Redirect after POST 

from django.shortcuts import render
from django.http import HttpResponseRedirect
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required
from models import Spot
from forms import SpotForm

def spots(request):
    spot_list = Spot.objects.all()
    return render(request, 'spots/spot_list.html', {'item_list': spot_list})

def spot_profile(request, spot_slug):
    s = get_document_or_404(Spot, slug=spot_slug)
    
    return render(request, 'spots/spot_profile.html', {'spot': s})

def new_spot(request):
    if request.method == 'POST': # If the form has been submitted...
        form = SpotForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/spots/') # Redirect after POST
    else:
        form = SpotForm() # An unbound form

    return render(request, 'spots/new_spot.html', {
        'form': form,
    })


from django.shortcuts import render
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required
from models import Spot

def spots(request):
    spot_list = Spot.objects.all()
    return render(request, 'spots/spot_list.html', {'item_list': spot_list})

def spot_profile(request, spot_slug):
    s = get_document_or_404(Spot, slug=spot_slug)
    
    return render(request, 'spots/spot_profile.html', {'spot': s})

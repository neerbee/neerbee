from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from atasteofathens.spots.models import Spot

def index(request):
    if request.user.is_authenticated():
        return render(request, 'spots/user_profile.html', {'user': request.user})
    else:
        return render(request, 'spots/index.html')

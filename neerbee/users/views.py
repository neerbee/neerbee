from django.shortcuts import render
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required
#from mongoengine.django.auth import User
#from neerbee.users.models import Bee

def user_home(request):
    if request.user.is_authenticated():
        return render(request, 'users/home.html', {'user': request.user})
    else:
        return render(request, 'index.html')


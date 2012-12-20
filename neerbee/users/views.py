from django.shortcuts import render
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required
#from mongoengine.django.auth import User
#from neerbee.users.models import Bee

@login_required
def user_home(request):
    return render(request, 'users/home.html', {'user': request.user})


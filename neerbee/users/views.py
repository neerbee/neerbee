from django.shortcuts import render
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required

def user_home(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render(request, 'users/home.html', {'user': request.user})

@login_required
def user_settings(request):
    return render(request, 'users/settings.html', {'user': request.user})


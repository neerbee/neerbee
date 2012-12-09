from django.shortcuts import render
from mongoengine.django.shortcuts import get_document_or_404
from django.contrib.auth.decorators import login_required
from mongoengine.django.auth import User
from spots.models import Spot

def index(request):
    if request.user.is_authenticated():
        return render(request, 'spots/user_profile.html', {'user': request.user})
    else:
        return render(request, 'spots/index.html')

@login_required
def users(request):
    user_list = User.objects.all()
    return render(request, 'spots/user_list.html', {'user_list': user_list})

@login_required
def user_profile(request, user_name):
    u = get_document_or_404(User, username=user_name)
    return render(request, 'spots/user_profile.html', {'user': u})

#@login_required
#def user_rate(request, user_name):
#    u = get_document_or_404(User, username=user_name)
    #all_items = Restaurant.objects.all()

   # user_ratings = [(i.restaurant, i.rating_value) for i in u.u_ratings.all()]
    #rated_items = [x[0] for x in user_ratings]
    #no_rating = [(i, None) for i in all_items if i not in rated_items]

    #user_ratings = user_ratings + no_rating
    #user_ratings.sort(key=lambda item: item[0].name)
#    return render(request, 'spots/user_rate.html', 
#                             {'user': u,
#                              'user_ratings': user_ratings})

def spots(request):
    spot_list = Spot.objects.all()
    return render(request, 'spots/spot_list.html', {'item_list': spot_list})

def spot_profile(request, spot_slug):
    s = get_document_or_404(Spot, slug=spot_slug)
    
    return render(request, 'spots/spot_profile.html', {'spot': s})

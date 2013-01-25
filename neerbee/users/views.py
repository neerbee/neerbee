from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.utils.translation import get_language_from_request

from mongoengine.django.shortcuts import get_document_or_404
from braces.views import LoginRequiredMixin

from .forms import UserSettingsForm
from .models import Bee

class IsStaffMixin(object):
    """
    Mixin that checks if user is staff member.
    """
    redirect_field_name = '/'
    login_url = settings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            msg = 'Need to be staff to do this.'
            messages.error(request, msg)
            return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(IsStaffMixin, self).dispatch(request,
                                                    *args, **kwargs)


class UserHomeView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():       
            return render(request, 'index.html')
        else:
            return render(request, 'users/home.html', {'user': request.user})


class UserSettingsView(LoginRequiredMixin, TemplateView):
	template_name = "users/settings.html"

	def get(self, request, *args, **kwargs):
            user = get_document_or_404(Bee, username=request.user.username)
            if not request.user.preferred_language:
                user.preferred_language = get_language_from_request(request)

            form = UserSettingsForm(initial=user._data)
	    return render(request, self.template_name, { 
                            'user': request.user,
                            'form': form
                         })

        def post(self, request, *args, **kwargs):
            form = UserSettingsForm(request.POST)
            user = get_document_or_404(Bee, username=request.user.username)

            if form.is_valid():
                user.preferred_language = form.cleaned_data.get(
                                                'preferred_language')
                user.save()
                # start using new language from current session
                request.session['django_language'] = user.preferred_language
                msg = 'User settings updated!'
                messages.info(request, msg)
                return HttpResponseRedirect('/')

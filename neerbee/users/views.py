from django.shortcuts import render
from django.views.generic import View, TemplateView

from braces.views import LoginRequiredMixin


class UserHomeView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():       
            return render(request, 'index.html')
        else:
            return render(request, 'users/home.html', {'user': request.user})


class UserSettingsView(LoginRequiredMixin, TemplateView):
	template_name = "users/settings.html"

	def get(self, request, *args, **kwargs):
	    return render(request, self.template_name, {'user': request.user})

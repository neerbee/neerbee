from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from users.views import IsStaffMixin
from users.models import Bee

class AdminPanelView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = "admin/admin_panel.html"

class UserListView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = "admin/user_list.html"
    
    def get_context_data(self, **kwargs):
        user_list = Bee.objects.order_by('username')
        return {'item_list': user_list}
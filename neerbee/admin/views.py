from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from users.views import IsStaffMixin

class AdminPanelView(LoginRequiredMixin, IsStaffMixin, TemplateView):
    template_name = "admin/admin_panel.html"
    
    #def get_context_data(self, **kwargs):
    #    spot_list = Spot.objects.order_by('name')
    #    return {'item_list': spot_list}

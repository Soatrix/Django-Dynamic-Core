from django.views.generic import TemplateView, View

# Create your views here.
class AdminDashboardHome(TemplateView):
    template_name = "adminpanel/dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAGE_TITLE"] = 'Admin Dashboard'
        return context
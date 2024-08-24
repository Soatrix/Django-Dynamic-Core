from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from panel.models import Theme
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError

# Create your views here.
class AdminDashboardHome(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAGE_TITLE"] = 'Admin Dashboard'
        return context

class AdminThemesView(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/themes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAGE_TITLE"] = "Manage Themes"
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if "create-theme" in request.POST:
            requiredFields = ["theme-name"]
            fields = ["theme-name", "theme-light-css", "theme-dark-css"]
            started = False
            for field in fields:
                if field not in request.POST:
                    if not started:
                        started = True
                        context["error"] = "<ul>"
                    context["error"] = context["error"] + f"<li>{field} is required."
                elif field in request.POST and field in requiredFields and request.POST.get(field) == "":
                    if not started:
                        context["error"] = "<ul>"
                        started = True
                    context["error"] = context["error"] + f"<li>The field \"" + field.replace("-", " ").replace("_", " ").title() + "\" is required.</li>"
            if started:
                context["error"] = context["error"] + "</ul>"
            saveRequired = False
            if not "error" in context:
                try:
                    theme = Theme.objects.create(name=request.POST.get("theme-name"), light_css=request.POST.get("theme-light-css"), dark_css=request.POST.get("theme-dark-css"))
                    saveRequired = True
                except IntegrityError:
                    context["success"] = False
                    context["error"] = "A theme with that name already exists. Please choose a different name."

            if saveRequired:
                theme.save()
                context["success"] = True
        return self.render_to_response(context)

class AdminThemeDetailView(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/theme-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["THEME"] = get_object_or_404(Theme, id=self.kwargs["id"])
        context["PAGE_TITLE"] = "Edit Theme #" + str(self.kwargs["id"])
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if "update-theme" in request.POST:
            requiredFields = ["name"]
            fields = ["name", "light_css", "dark_css"]
            started = False
            for field in fields:
                if field not in request.POST:
                    if not started:
                        started = True
                        context["error"] = "<ul>"
                    context["error"] = context["error"] + f"<li>{field} is required."
                elif field in request.POST and field in requiredFields and request.POST.get(field) == "":
                    if not started:
                        context["error"] = "<ul>"
                        started = True
                    context["error"] = context["error"] + f"<li>The field \"" + field.replace("-", " ").replace("_", " ").title() + "\" is required.</li>"
            if started:
                context["error"] = context["error"] + "</ul>"
            saveRequired = False
            if not "error" in context:
                for field in fields:
                    setattr(context["THEME"], field, request.POST.get(field))
                    saveRequired = True
            if saveRequired:
                context["THEME"].save()
                context["success"] = True
        elif "delete-theme" in request.POST:
            context["THEME"].delete()
            return redirect("admin-themes")
        return self.render_to_response(context)

class AdminUsersView(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAGE_TITLE"] = "Manage Users"
        context["USERS"] = User.objects.all()
        return context

class AdminGroupsView(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/groups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PAGE_TITLE"] = "Manage Groups"
        context["GROUPS"] = Group.objects.all()
        return context

class AdminGroupDetailView(LoginRequiredMixin, TemplateView):
    template_name = "adminpanel/group-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["GROUP"] = get_object_or_404(Group, id=self.kwargs["id"])
        context["PERMISSIONS"] = Permission.objects.all()
        context["PAGE_TITLE"] = "Edit Group #" + str(self.kwargs["id"])
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        saveRequired = False
        print(request.POST)
        for permission in context["PERMISSIONS"]:
            if "permission-" + str(permission.id) in request.POST:
                if permission not in context["GROUP"].permissions.all():
                    context["GROUP"].permissions.add(permission)
                    saveRequired = True
            else:
                if permission in context["GROUP"].permissions.all():
                    context["GROUP"].permissions.remove(permission)
                    saveRequired = True
        if saveRequired:
            context["GROUP"].save()
            context["success"] = True
        return self.render_to_response(context)
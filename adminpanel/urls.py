from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', AdminDashboardHome.as_view(), name="admin-dashboard-home"),
    path('admin/users/', AdminUsersView.as_view(), name="admin-users"),
    path('admin/themes/', AdminThemesView.as_view(), name="admin-themes"),
    path('admin/themes/edit/<int:id>/', AdminThemeDetailView.as_view(), name='admin-theme-detail'),
]
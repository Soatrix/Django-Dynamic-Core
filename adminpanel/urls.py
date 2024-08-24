from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', AdminDashboardHome.as_view(), name="admin-dashboard-home")
]
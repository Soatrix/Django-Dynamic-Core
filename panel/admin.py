from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
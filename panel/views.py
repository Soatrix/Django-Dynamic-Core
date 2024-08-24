from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.text import slugify
from .models import *
import json

# Create your views here.
class Dashboard404View(TemplateView):
    template_name = "404.html"
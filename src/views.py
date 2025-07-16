from django.shortcuts import render

from django.views.generic import ListView
from .models import *
# Create your views here.
class HomeView(ListView):
    template_name = "src/home.html"
    context_object_name = 'mydata'
    model = Locations
    #form_class = EmailForm
    success_url = "/"
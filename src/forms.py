from django import forms
from django.forms import ModelForm
from .models import *

modes = (
    ("driving", "driving"),
    ("walking", "walking"),
    ("bicycling", "bicycling"),
    ("transit", "transit")
)
class DistanceForm(ModelForm):
    # define inputs
    from_location = forms.ModelChoiceField(label = "Location form", required = True, queryset = Locations.objects.all())
    to_location =  forms.ModelChoiceField(label = "Location form", required = True, queryset = Locations.objects.all())
    mode = forms.ChoiceField(choices = modes, required = True)
    class Meta:
        model = Distances
        exclude = ['created_at', 'edited_at', 'distance_km', 'duration_mins', 'duration_traffic_mins'] # specify fields we will not have in form
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import *
from django.conf import settings
import googlemaps


# Create your views here.
class HomeView(ListView):
    template_name = "src/home.html"
    context_object_name = 'mydata'
    model = Locations
    #form_class = EmailForm
    success_url = "/"

class GeocodingView(View):
    template_name = "src/geocoding.html"

    def get(self, request, pk):
        location = Locations.objects.get(pk=pk)
        # do not use API if lat, long, and place_id already exist in the database
        if location.lng and location.lat and location.place_id != None:
            latitude = location.lat
            longitude = location.lng
            place_id = location.place_id
            label = "from my database"

        # get infromation from the API
        elif location.address and location.country and location.zipcode and location.city != None:
            address_string = str(location.address) + ", " + str(location.zipcode) + ", " + str(location.city)+ ", " + str(location.country) # string of info to pass into api
            # print(address_string)
            # create JSON file using google maps API
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY) 

            result = gmaps.geocode(address_string)[0] # JSON file containing a dictionary with important geolocation data
            geometry = result.get('geometry', {})
            location1 = geometry.get('location', {})
            latitude = location1.get('lat', {}) # access latitude key in location1 dictionary
            longitude = location1.get('lng', {})
            place_id = result.get('place_id', {})
            label = "from my API call"
            # add json file information to the model in the database
            location.lat = latitude
            location.lng = longitude
            location.place_id = place_id
            location.save()

        # make field empty if API doesnt work
        else: 
            result = ""
            latitude = ""
            longitude = ""
            place_id = ""
            label = "no API call made"
            
        # context adds variables to the html template file
        context = {
            'location':location,
            # 'result':result,
            # 'geometry':geometry,
            # 'location1':location1,
            'latitude':latitude,
            'longitude':longitude,
            'place_id':place_id,
            'label':label,
        }
        return render(request, self.template_name, context)
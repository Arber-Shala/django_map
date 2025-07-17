from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from .models import *
from .forms import *
from django.conf import settings
import googlemaps
from datetime import datetime


# Create your views here.
class HomeView(ListView):
    template_name = "src/home.html"
    context_object_name = 'mydata'
    model = Locations
    #form_class = EmailForm
    success_url = "/"

class DistanceView(View):
    template_name = "src/distance.html"

    def get(self, request):
        form = DistanceForm
        distances = Distances.objects.all()
        context = {
            'form':form,
            'distances':distances
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
            print("it's valid")
            from_location = form.cleaned_data['from_location'] # get info from the form
            from_location_info = Locations.objects.get(name=from_location)
            from_address_string = str(from_location_info.address) + ", " + str(from_location_info.zipcode) + ", " + str(from_location_info.city) + ", " + str(from_location_info.country)
            
            to_location = form.cleaned_data['to_location']
            to_location_info = Locations.objects.get(name=to_location)
            to_address_string = str(to_location_info.address) + ", " + str(to_location_info.zipcode) + ", " + str(to_location_info.city) + ", " + str(to_location_info.country) 

            mode = form.cleaned_data['mode']

            now = datetime.now() # get current data to get traffic time

            # API call
            gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)

            # output JSON dictionary of distance between two locations
            calculate = gmaps.distance_matrix(
                from_address_string,
                to_address_string,
                mode = mode,
                departure_time = now
            )
            # access information from JSON dictaionry
            duration_seconds = calculate['rows'][0]['elements'][0]['duration']['value']
            duration_minutes = duration_seconds/60

            distance_meters = calculate['rows'][0]['elements'][0]['distance']['value']
            distance_kilometers = duration_seconds/1000

            if('duration_in_traffic' in calculate['rows'][0]['elements'][0]):
                duration_in_traffic_seconds =  calculate['rows'][0]['elements'][0]['duration_in_traffic']['value']
                duration_in_traffic_minutes = duration_in_traffic_seconds/60
            else:
                duration_in_traffic_minutes = None
            # save variables to a distances model
            obj = Distances(
                from_location = Locations.objects.get(name=from_location),
                to_location = Locations.objects.get(name = to_location),
                mode = mode,
                distance_km = distance_kilometers,
                duration_mins = duration_minutes,
                duration_traffic_mins = duration_in_traffic_minutes,
            )
            obj.save()
        else:
            print(form.errors)
        return redirect('my_distance_view')

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
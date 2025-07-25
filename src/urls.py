from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name='my_home_view'),
    path("geocoding/<int:pk>", GeocodingView.as_view(), name='my_geocoding_view'),
    path("distance/<int:pk>", DistanceView.as_view(), name='my_distance_view'),
]
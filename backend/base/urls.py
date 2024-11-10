from django.urls import path
from . import airline_views
from . import aircraft_views


urlpatterns = [
    path('airline/', airline_views.airline_list),
    path('airline/<int:pk>', airline_views.airline_detail),

    path('aircraft/', aircraft_views.aircraft_list),
    path('aircraft/<int:pk>', aircraft_views.aircraft_detail),
]
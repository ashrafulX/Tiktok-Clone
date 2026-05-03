from django.urls import path
from .views import *

urlpatterns = [
    path('', search,name= "search"),
    path('search_suggestions/', search_suggestions,name= "search_suggestions"),
]

from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', notifications,name= "notifications"),
    path('newnotifications/', newnotifications,name= "newnotifications"),
]

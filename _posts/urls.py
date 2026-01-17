from django.contrib import admin
from django.urls import path
from .views import home, explore

urlpatterns = [
    path('', home,name= "home"),
    path('explore/', explore,name= "explore"),  
]

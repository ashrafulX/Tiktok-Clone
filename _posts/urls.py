from django.contrib import admin
from django.urls import path
from .views import home, explore, upload

urlpatterns = [
    path('', home,name= "home"),
    path('explore/', explore,name= "explore"),
    path('upload/', upload,name= "upload"),
]

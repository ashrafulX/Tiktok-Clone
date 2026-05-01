from django.urls import path
from .views import *

urlpatterns = [
    path('<username>/', follow,name= "follow"),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', following_view,name= "following"),
    path('friends/', friends_view,name= "friends"),
    path('<username>/', follow,name= "follow"),
]

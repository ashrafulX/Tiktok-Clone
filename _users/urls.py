from django.urls import path
from .views import profile_view, index_view

urlpatterns = [
    path('@<username>/', profile_view,name= "profile"),
    path('login/', index_view,name= "index"),
]

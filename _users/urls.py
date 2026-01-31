from django.urls import path
from .views import profile_view, index_view, profile_edit

urlpatterns = [
    path('@<username>/', profile_view,name= "profile"),
    path('login/', index_view,name= "index"),
    path('/profile/', profile_view),
    path('/profile/edit/', profile_edit,name= "profile_edit"),
]

from django.urls import path
from .views import profile_view, index_view, profile_edit, settings_view, delete_account

urlpatterns = [
    path('@<username>/', profile_view,name= "profile"),
    path('login/', index_view,name= "index"),
    path('profile/', profile_view),
    path('profile/edit/', profile_edit,name= "profile_edit"),
    path('profile/settings/', settings_view,name= "settings"),
    path('profile/delete_account/', delete_account,name= "delete_account"),
]

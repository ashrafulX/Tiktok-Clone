from django.contrib import admin
from django.urls import path
from .views import home, explore, upload, post_page_view, verification_code

urlpatterns = [
    path('', home,name= "home"),
    path('explore/', explore,name= "explore"),
    path('upload/', upload,name= "upload"),
    path('post/<pk>/', post_page_view, name='post_page'),
    path('verification_code/', verification_code, name='verification_code'),
    path('post/', post_page_view)
]

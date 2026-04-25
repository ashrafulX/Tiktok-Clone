from django.contrib import admin
from django.urls import path
from .views import home, explore, upload, post_page_view, verification_code, post_edit, like_post, bookmark_post

urlpatterns = [
    path('', home,name= "home"),
    path('explore/', explore,name= "explore"),
    path('upload/', upload,name= "upload"),
    path('post/<pk>/', post_page_view, name='post_page'),
    path('verification_code/', verification_code, name='verification_code'),
    path('post/', post_page_view),
    path('post_edit/<pk>/', post_edit, name='post_edit'),
    path('like/<pk>/', like_post, name='like_post'),
    path('bookmark/<pk>/', bookmark_post, name='bookmark_post'),
]

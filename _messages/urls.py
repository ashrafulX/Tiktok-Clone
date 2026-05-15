from django.urls import path
from .views import *

urlpatterns = [
    path('', messages,name= "messages"),
    path('conversations/', conversations,name= "conversations"),
    path('chat/<receiver_id>', chat,name= "chat"),
]

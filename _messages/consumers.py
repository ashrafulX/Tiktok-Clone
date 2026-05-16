from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.template.loader import render_to_string

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        
        if not self.user or not self.user.is_authenticated:
            self.close()
            return
        
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"
        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        
    def broadcast_message(self, event):
        message = Message.objects.get(id=event["message_id"])
        context = {
            "message": message,
            "user": self.user
        }
        
        html_response = render_to_string("_messages/partials/_message_oob.html", context)
        self.send(text_data=html_response)
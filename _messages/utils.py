from .models import Conversation, ConvUser
from django.db.models import Count


def get_or_create_conversation(user1, user2=None):
    if user2 is None or user1 == user2:
        conversation = Conversation.objects.annotate(
            num_participants=Count('participants')
        ).filter(
            num_participants=1,
            participants=user1
        ).first()
        if conversation is None:
            conversation = Conversation.objects.create()
            ConvUser.objects.create(conversation=conversation, user=user1)
    else:
        conversation = Conversation.objects.filter(participants=user1).filter(participants=user2).first()
    return conversation
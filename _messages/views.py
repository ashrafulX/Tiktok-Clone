from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .utils import get_or_create_conversation

User = get_user_model()

@login_required
def messages(request):
    context = {
        'page': 'Messages',
    }
    
    return render(request, '_messages/messages_page.html', context)

@login_required
def conversations(request):
    
    get_or_create_conversation(request.user)
    
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    
    conversations_extended = []
    for conversation in conversations:
        is_self = conversation.participants.count() == 1
        if is_self:
            receiver = request.user
        else:
            receiver = conversation.participants. exclude (pk=request.user.pk).first()
            
        conversations_extended.append({
            'conversation': conversation,
            'receiver': receiver,
            'is_self': is_self,
        })
    
    context = {
        'conversations': conversations_extended,
    }
    
    return render(request, '_messages/conversations.html', context)

@login_required
def chat(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver and receiver != request.user:
        chat = get_or_create_conversation(request.user, receiver)
        is_self = False
    else:
        chat = get_or_create_conversation(request.user)
        is_self = True
        
    messages = Message.objects.filter(conversation=chat).order_by('created_at')[:100]
    
    context = {
        'Page': 'Messages',
        'receiver': receiver,
        'chat': chat,
        'is_self': is_self,
        'messages': messages
    }
    
    return render(request, '_messages/chat.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


@login_required
def follow(request, username=None):
    print("eeeeeeeeeeeeeeeeeeeeeeeeee")
    this_user = get_object_or_404(User, username=username)
    
    if this_user == request.user:
        return HttpResponse()
    
    follow_object, created = Follow.objects.get_or_create(follower=request.user, following=this_user)
    
    if not created:
        follow_object.delete()
    

    context = {
        'this_user': this_user,
        'follow_clicked': True
    }
    
    if request.GET.get('follow_round'):
        return render(request, '_network/partials/_follow_round.html', context)
    
    if request.htmx:
        return render(request, '_network/partials/_follow_button.html', context)

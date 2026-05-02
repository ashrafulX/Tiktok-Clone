from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow
from django.db.models import Count

User = get_user_model()

@login_required
def following_view(request):
    following_ids = request.user.is_follower.values_list('following', flat=True)
    following_users = User.objects.filter(id__in=following_ids)
    
    not_following_users = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id)
    suggested_users = not_following_users.annotate(total_likes=Count('posts__likes', distinct=True)).order_by('-total_likes')[:10]
    
    context = {
        'page': 'Following',
        'following_users': following_users,
        'suggested_users': suggested_users,
    }
    
    if request.htmx:
        return render(request, '_network/partials/_following.html', context)
    
    return render(request, '_network/following.html', context)

@login_required
def friends_view(request):
    following_ids = request.user.is_follower.values_list('following', flat=True)
    followers_ids = request.user.is_followed.values_list('follower', flat=True)
    friends_ids = set(following_ids) & set(followers_ids)
    friends = User.objects.filter(id__in=friends_ids).order_by('username')
    suggested_friends = User.objects.filter(id__in=followers_ids).exclude(id__in=friends_ids).order_by('username')[:10]
    
    context = {
        'page': 'Friends',
        'friends': friends,
        'suggested_friends': suggested_friends,
    }
    
    if request.htmx:
        return render(request, '_network/partials/_friends.html', context)
    
    return render(request, '_network/friends.html', context)

@login_required
def follow(request, username=None):
    this_user = get_object_or_404(User, username=username)
    
    if this_user == request.user:
        return HttpResponse()
    
    follow_object, created = Follow.objects.get_or_create(follower=request.user, following=this_user)
    
    if not created:
        follow_object.delete()
    

    context = {
        'this_user': this_user,
        'follow_clicked': True,
        'modal': request.GET.get('modal', False),
    }
    
    if request.GET.get('follow_round'):
        return render(request, '_network/partials/_follow_round.html', context)
    if request.GET.get('follow_rounded'):
        return render(request, '_network/partials/_follow_rounded.html', context)
    
    if request.htmx:
        return render(request, '_network/partials/_follow_button.html', context)

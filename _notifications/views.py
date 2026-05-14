from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from _network.models import Follow
from _posts.models import LikedPost, LikedComment, Comment, Repost
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from .models import NotificationTracker
from django.utils import timezone

@login_required
def notifications(request):
    
    tracker, created = NotificationTracker.objects.get_or_create(user=request.user)
    
    if tracker.activity_last_seen is None:
        welcome_message = "Welcome! This is where you'll see likes, comments, and follows."
    else:
        welcome_message = None
        
    tracker.activity_last_seen = timezone.now()
    tracker.save(update_fields=['activity_last_seen'])
    
    followers = Follow.objects.filter(
                    following=request.user
                ).select_related('follower').order_by('-created_at')[:10]
    
    liked_posts = LikedPost.objects.filter(
                    post__author=request.user
                ).exclude(user=request.user).select_related('user','post').order_by('-created_at')[:10]
    
    liked_comments = LikedComment.objects.filter(
                    comment__author=request.user
                ).exclude(user=request.user).select_related('user','comment','comment__post').order_by('-created_at')[:10]
    
    comments = Comment.objects.filter(
                    post__author=request.user,
                    parent_comment__isnull=True
                ).exclude(author=request.user).select_related('author','post').order_by('-created_at')[:10]
    
    replies = Comment.objects.filter(
                    Q(parent_comment__author=request.user) | 
                    Q(parent_reply__author=request.user)
                ).exclude(author=request.user).select_related('author','post','parent_comment').order_by('-created_at')[:10]
    
    reposts = Repost.objects.filter(
                    post__author=request.user
                ).exclude(user=request.user).select_related('user','post').order_by('-created_at')[:10]
    
    combined_notifications = sorted(
        chain(followers, liked_posts, liked_comments, comments, replies, reposts),
        key=attrgetter('created_at'),
        reverse=True
    )
    
    notifications = combined_notifications[:20]
    
    print("notifications")
    print(welcome_message)
    
    context = {
        'notifications': notifications,
        'welcome_message': welcome_message
    }
    
    return render(request, '_notifications/notifications.html', context)

@login_required
def new_notifications(request):
    tracker, created = NotificationTracker.objects.get_or_create(user=request.user)
    last_seen = tracker.activity_last_seen
    has_new_notifications = True
    
    if last_seen:
        has_new_notifications = (
            Follow.objects.filter(
                following=request.user,
                created_at__gt=last_seen
            ).exists() 
            
            or LikedPost.objects.filter(
                post__author=request.user,
                created_at__gt=last_seen    
            ).exclude(user=request.user).exists()
            
            or LikedComment.objects.filter(
                comment__author=request.user,
                created_at__gt=last_seen    
            ).exclude(user=request.user).exists()
            
            or Comment.objects.filter(
                Q(post__author=request.user) |
                Q(parent_comment__author=request.user) |
                Q(parent_reply__author=request.user),
                created_at__gt=last_seen
            ).exclude(author=request.user).exists()
            
            or Repost.objects.filter(
                post__author=request.user,
                created_at__gt=last_seen
            ).exclude(user=request.user).exists()
        )
    
    context = {
        'has_new_notifications': has_new_notifications,
    }
    
    
    return render(request, '_notifications/notify_dot.html', context)
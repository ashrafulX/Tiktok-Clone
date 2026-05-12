from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from _network.models import Follow
from _posts.models import LikedPost, LikedComment, Comment, Repost
from django.db.models import Q
from itertools import chain
from operator import attrgetter

@login_required
def notifications(request):
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
    print(notifications)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, '_notifications/notifications.html', context)
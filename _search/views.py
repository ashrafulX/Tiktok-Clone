from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from _posts.models import Post, Tag

User = get_user_model()

@login_required
def search(request):
    query = request.GET.get('q', None)
    
    users = User.objects.none()
    posts = Post.objects.none()
    
    if query and len(query) > 2:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) |
            Q(bio__icontains=query)
        ).order_by('username')
        
        posts = Post.objects.filter(
            Q(body__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')

    context = {
        'users': users,
        'posts': posts,
    }
    
    if request.htmx:
        return render(request, '_search/partials/_search_page.html', context)
    
    return render(request, '_search/search_page.html', context)

@login_required
def search_suggestions(request):
    query = request.GET.get('q', None)
    
    hashtags_upload = request.GET.get('tags')
    if hashtags_upload:
        if hashtags_upload.endswith(' '):
            query = ""
        else:
            query = hashtags_upload.split()[-1].lstrip('#')
    
    user_suggestions = User.objects.none()
    tag_suggestions = User.objects.none()
    
    if query and len(query) > 2:
        user_suggestions = User.objects.filter(
            Q(username__icontains=query) |
            Q(name__icontains=query) |
            Q(bio__icontains=query)
        ).annotate(followers_count=Count('is_followed', distinct=True)).order_by('-followers_count')[:5]
        
        tag_suggestions = Tag.objects.filter(name__istartswith=query)[:5]
    
    context = {
        'user_suggestions': user_suggestions,
        'tag_suggestions': tag_suggestions,
    }
    
    if hashtags_upload:
        return render(request, '_search/partials/_hashtag_suggestions.html', context)
    
    return render(request, '_search/partials/_search_suggestions.html', context)
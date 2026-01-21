from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home(request):
    posts = Post.objects.order_by('-created_at')
    
    paginator = Paginator(posts, 1)
    page_number = int(request.GET.get('page_number', 1))
    posts_page = paginator.get_page(page_number)
    next_page = posts_page.next_page_number() if posts_page.has_next() else None
    page_start_index = (posts_page.number - 1 ) * paginator.per_page
    
    context = {
        'page' : 'Home',
        'posts': posts_page,
        'next_page': next_page,
        'page_start_index': page_start_index
    }
    
    if request.GET.get('paginator'):
        return render(request, '_posts/partials/_posts.html', context)
    
    if request.htmx:
        return render(request, '_posts/partials/_home.html', context)
    return render(request, '_posts/home.html', context)

def explore(request):
    posts = Post.objects.order_by('-created_at')
    context = {
        'page' : 'Explore',
        'posts': posts
    }
    if request.htmx:
        return render(request, '_posts/partials/_explore.html', context)
    return render(request, '_posts/explore.html', context)

@login_required
def upload(request):
    form = PostForm()
    
    if request.method ==  'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
        
    context = {
        'page' : 'Upload',
        'form' : form
    }
    
    if request.htmx:
        return render(request, '_posts/partials/_upload.html', context)
    return render(request, '_posts/upload.html', context)
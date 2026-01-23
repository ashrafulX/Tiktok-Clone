from django.shortcuts import render, redirect, get_object_or_404
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


def post_page_view(request, pk=None):
    
    if not pk:
        return redirect('home')
    post = get_object_or_404(Post, uuid=pk)
    
    if post.author:
        author_posts = Post.objects.filter(author=post.author).order_by('-created_at')
        prev_post = author_posts.filter(created_at__gt=post.created_at).last()
        next_post = author_posts.filter(created_at__lt=post.created_at).first()
    else:
        author_posts = [ post ]
        prev_post = next_post = None 
    
    context = {
        'post' : post,
        'author_posts': author_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    
    if request.htmx:
        return render(request, '_posts/partials/_postpage.html', context)
    return render(request, '_posts/postpage.html', context)
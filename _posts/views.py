from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all()
    context = {
        'page' : 'Home',
        'posts': posts
    }
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
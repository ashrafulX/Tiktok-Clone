from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

User = get_user_model()

def index_view(request):
    return render(request, '_users/index.html')


@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', request.user.username)
    
    profile_user = get_object_or_404(User, username=username)
    
    sort_order = request.GET.get('sort','')
    
    if sort_order == 'oldest':
        profile_posts = profile_user.posts.order_by('created_at')
    else:
        profile_posts = profile_user.posts.order_by('-created_at')
    
    context = {
        'page' : 'Profile',
        'profile_user': profile_user,
        'profile_posts': profile_posts,
    }
    
    if request.GET.get('sort'):
        return render(request, '_users/partials/_profile_posts.html', context)

    if request.htmx:
        return render(request, '_users/partials/_profile.html', context)
    return render(request, '_users/profile.html', context)

@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
        
    context = {
        'form': form
    }
    
    if request.htmx:
        return render(request, '_users/partials/_profile_edit.html', context=context)
    return redirect('profile', request.user.username)
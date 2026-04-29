from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ProfileForm, EmailForm, BirthdayForm
from allauth.account.models import EmailAddress
from django.core.cache import cache
from django.http import HttpResponse
from django.db.models import Count

User = get_user_model()

def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, '_users/index.html')

@login_required
def profile_view(request, username=None):
    if not username:
        return redirect('profile', request.user.username)
    
    profile_user = get_object_or_404(User, username=username)
    
    if request.GET.get('link'):
        urlpath = reverse('profile', kwargs={'username': username})
        return render(request, '_users/partials/_profile_link.html', {'urlpath': urlpath})
    
    if request.GET.get('reposted'):
        profile_posts_reposted = profile_user.repostedposts.all().order_by('-repost__created_at')
        return render(request, '_users/partials/_profile_posts_reposted.html', {"profile_posts_reposted": profile_posts_reposted})
    
    if request.GET.get('liked'):
        profile_posts_liked = profile_user.liked_posts.all().order_by('-likedpost__created_at')
        return render(request, '_users/partials/_profile_posts_liked.html', {"profile_posts_liked": profile_posts_liked})
    
    profile_posts = profile_user.posts.order_by('-created_at')
    if request.GET.get('sort'):
        sort_order = request.GET.get('sort','')
        if sort_order == 'oldest':
            profile_posts = profile_user.posts.order_by('created_at')
        elif sort_order == 'popular':
            profile_posts = profile_user.posts.annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')
        else:
            profile_posts = profile_user.posts.order_by('-created_at')
        return render(request, '_users/partials/_profile_posts.html', {"profile_posts": profile_posts})
    
    if request.GET.get('bookmarked'):
        profile_posts_bookmarked = {}
        if request.user == profile_user:
            profile_posts_bookmarked = profile_user.bookmarkedposts.all().order_by('-bookmarkedpost__created_at')
        return render(request, '_users/partials/_profile_posts_bookmarked.html', {"profile_posts_bookmarked": profile_posts_bookmarked})
        
    profile_user_likes = profile_user.posts.aggregate(total_likes=Count('likes'))['total_likes']
    
    context = {
        'page' : 'Profile',
        'profile_user': profile_user,
        'profile_user_likes': profile_user_likes,
        'profile_posts': profile_posts
    }
    
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

@login_required
def settings_view(request):
    
    form = EmailForm(instance=request.user)
    
    if request.GET.get('email'):
        return render(request, '_users/partials/_settings_email.html', {'form':form})
    
    if request.POST.get('email'):
        form = EmailForm(request.POST, instance=request.user)
        current_email = request.user.email
        
        if form.is_valid():
            new_email = form.cleaned_data['email']
            if new_email != current_email:
                form.save()
                email_obj = EmailAddress.objects.get(user=request.user, primary=True)
                email_obj.email = new_email
                email_obj.verified = False
                email_obj.save()
                return redirect('settings')
            
    if request.GET.get('verification'):
        return render(request, '_users/partials/_settings_verification.html', {'form':form})
    
    if request.POST.get('code'):
        code = request.POST.get('code')
        email = request.user.email
        cached_code = cache.get(f"verification_code_{email}")
        if cached_code and cached_code == code:
            email_obj = EmailAddress.objects.get(user=request.user, primary=True)
            email_obj.verified = True
            email_obj.save()
            return redirect('settings')
        
    if request.GET.get('birthday'):
        birthdayForm = BirthdayForm(instance=request.user)
        return render(request, '_users/partials/_settings_birthday.html', {'form':birthdayForm})
    
    if request.POST.get('birthday'):
        birthdayForm = BirthdayForm(request.POST, instance=request.user)
        
        if birthdayForm.is_valid():
            birthdayForm.save()
            return redirect('settings')
    
    if request.POST.get("notifications"):
        print(request.POST.get("notifications"))
        if request.POST.get("notifications") == 'on':
            request.user.notifications = True
        else:
            request.user.notifications = False
        request.user.save()
        return HttpResponse('')
    
    if request.GET.get("darkmode"):
        if request.GET.get("darkmode") == 'true':
            request.user.darkmode = True
        else:
            request.user.darkmode = False
        request.user.save()
        return HttpResponse('')
    
    if request.htmx:
        return render(request, '_users/partials/_settings.html', {'form':form})
    return render(request, '_users/settings.html', {'form':form})

@login_required
def delete_account(request):
    user = request.user 
    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect('home')
        
    return render(request, '_users/profile_delete.html')
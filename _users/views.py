from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, EmailForm, BirthdayForm
from allauth.account.models import EmailAddress
from django.core.cache import cache
from django.http import HttpResponse

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

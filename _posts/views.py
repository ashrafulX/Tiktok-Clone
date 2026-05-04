from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PostForm, PostEditForm
from .models import Post, Comment, Repost
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.validators import validate_email
import secrets
import threading
from django.core.cache import cache
from django.core.mail import EmailMessage
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db.models import Count
from itertools import chain
from operator import attrgetter
from .utils import process_tags

User = get_user_model()


@login_required
def home(request):
    following_user_ids = request.user.is_follower.values_list('following', flat=True)
    user_ids = list(following_user_ids) + [request.user.id]
    posts = Post.objects.filter(author__in=user_ids).order_by('-created_at')
    reposts = Repost.objects.filter(user__in=user_ids).select_related('post', 'user')
    
    reposted_posts = []
    for repost in reposts:
        post = repost.post
        post.created_at = repost.created_at
        post.repost_author = repost.user
        post.is_repost = True
        reposted_posts.append(post)
    
    feed = sorted(
        chain(posts, reposted_posts),
        key = attrgetter('created_at'),
        reverse=True
    )
    
    paginator = Paginator(feed, 1)
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

@login_required
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
            input_tags = request.POST.get('tags','')
            process_tags(post, input_tags)
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
    
    if request.method == "POST":
        body = request.POST.get('comment')
        if body:
            Comment.objects.create(body=body, post=post, author=request.user)
            
        context = {
            'post' : post,
        }
        return render(request, '_posts/partials/comments/_comment_loop.html', context)
    
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

def verification_code(request):
    email = request.GET.get("email")
    if not email:
        return HttpResponse('<p class="error">Email is required.</p>')
    
    try:
        validate_email(email)
    except:
        return HttpResponse('<p class="error">Invalid email address provided.</p>')
    
    if not request.user.is_authenticated:
        if EmailAddress.objects.filter(email__iexact=email).exists() or \
        User.objects.filter(email__iexact=email).exists():
            return HttpResponse('<p class="error">This email is already in use.</p>')
    
    code = str(secrets.randbelow(900000) + 100000)
    cache.set(f"verification_code_{email}", code, timeout=300)
    subject = "Your TikTok Verification Code"
    message = f"Use this code to sign up: {code}. It expires in 5 minutes."
    sender = "no-reply@tiktok-clone.com"
    recipients = [email]

    email_thread = threading.Thread(target=send_mail_async, args=(subject, message, sender, recipients))
    email_thread.start()
    
    return HttpResponse('<p class="success">Verification code sent to your email!</p>')

def send_mail_async(subject, message, sender, recipients):
    email = EmailMessage(subject, message, sender, recipients)
    email.send()

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, uuid=pk)
    form = PostEditForm(instance=post)
    
    if post.author != request.user:
        return redirect('home')
    
    if request.method == "POST" and "delete" in request.POST:
        process_tags(post)
        post.delete()
        return redirect('profile', request.user.username)

    # EDIT
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            input_tags = form.cleaned_data.get('tags','')
            process_tags(post, input_tags)
            return redirect('post_page', pk)
    else:
        form = PostEditForm(instance=post)
        
    context = {
        'post': post,
        'form': form
    }
    
    if request.htmx:
        return render(request, '_posts/partials/_post_edit.html', context)
    return redirect('post_page', pk)

@login_required
def like_post(request, pk=None):
    post = get_object_or_404(Post, uuid=pk)
    
    if request.htmx:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            
    profile_user_likes = post.author.posts.aggregate(total_likes=Count('likes'))['total_likes']
    
    context = {
        'post': post,
        'profile_user_likes': profile_user_likes
    }
    
    if request.GET.get('home'):
        return render(request, '_posts/partials/_like_home.html', context)
    
    if request.GET.get('postpage'):
        return render(request, '_posts/partials/_like_postpage.html', context)
    
    return redirect('post_page', pk)

@login_required
def bookmark_post(request, pk=None):
    post = get_object_or_404(Post, uuid=pk)
    
    if request.htmx:
        if post.bookmarks.filter(id=request.user.id).exists():
            post.bookmarks.remove(request.user)
        else:
            post.bookmarks.add(request.user)
            
    context = {
        'post': post
    }
    
    if request.GET.get('home'):
        return render(request, '_posts/partials/_bookmark_home.html', context)
    
    if request.GET.get('postpage'):
        return render(request, '_posts/partials/_bookmark_postpage.html', context)
    
    return redirect('post_page', pk)

@login_required
def comment(request, pk=None):
    if not request.htmx:
        return redirect('home')
    
    comment = get_object_or_404(Comment, uuid=pk)
    
    parent_comment = comment
    while parent_comment.parent_comment is not None:
        parent_comment = parent_comment.parent_comment
        
    parent_reply = comment if comment.parent_comment else None
    
    print(request)
    if request.method == 'POST':
        print(request.POST)
        body = request.POST.get('reply')
        if body:
            Comment.objects.create(body=body, 
                                   author=request.user,
                                   post=comment.post,
                                   parent_reply=parent_reply,
                                   parent_comment=parent_comment)
            return redirect('comment', comment.uuid)
    
    context = {
        'comment': parent_comment,
        'current_comment': comment
    }
    
    if request.GET.get('hide_replies'):
        return render(request, '_posts/partials/comments/_button_view_replies.html', context)
    
    if request.GET.get('reply_form'):
        return render(request, '_posts/partials/comments/_form_add_reply.html', context)
    
    return render(request, '_posts/partials/comments/_reply_loop.html', context)

@login_required
def comment_delete(request, pk=None):
    if not request.htmx:
        return redirect('home')
    
    comment = get_object_or_404(Comment, uuid=pk)
    if comment.author != request.user:
        return HttpResponse()
    
    if request.method == 'POST':
        post = comment.post
        comment.delete()
        comment_count = post.comments.count()
        response = f"<div hx-swap-oob='innerHTML' id='comment_count'>{comment_count}</div>"
        return HttpResponse(response)
    
    context = {
        'comment': comment
    }
    
    return render(request, '_posts/partials/comments/_from_comment_delete.html', context)

@login_required
def comment_like(request, pk=None):
    
    comment = get_object_or_404(Comment, uuid=pk)
    
    if request.htmx:
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
            
    context = {
        'comment': comment
    }
    
    return render(request, '_posts/partials/comments/_button_like_comment.html', context)

@login_required
def share_post(request, pk=None):
    post = get_object_or_404(Post, uuid=pk)
    
    if request.GET.get('repost'):
        if post.reposts.filter(id=request.user.id).exists():
            post.reposts.remove(request.user)
        else:
            post.reposts.add(request.user)
        return redirect('home')
    
    context = {
        'post': post
    }
    
    print(post)
    
    if request.htmx:
        return render(request, '_posts/partials/_post_share.html', context)
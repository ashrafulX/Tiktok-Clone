from django.shortcuts import render

def home(request):
    context = {
        'page' : 'Home',
    }
    return render(request, '_posts/home.html', context)

def explore(request):
    context = {
        'page' : 'Explore',
    }
    return render(request, '_posts/explore.html', context)
from django.shortcuts import render

def home(request):
    context = {
        'page' : 'Home',
    }
    if request.htmx:
        return render(request, '_posts/partials/_home.html', context)
    return render(request, '_posts/home.html', context)

def explore(request):
    context = {
        'page' : 'Explore',
    }
    if request.htmx:
        return render(request, '_posts/partials/_explore.html', context)
    return render(request, '_posts/explore.html', context)

def upload(request):
    context = {
        'page' : 'Upload',
    }
    
    if request.htmx:
        return render(request, '_posts/partials/_upload.html', context)
    return render(request, '_posts/upload.html', context)
from django.shortcuts import render

def home(request):
    return render(request, '_posts/home.html')

def explore(request):
    return render(request, '_posts/explore.html')
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')

def detail(request, blog_id):
    return render(request, 'blog_detail.html')

def public(request):
    return render(request, 'public.html')


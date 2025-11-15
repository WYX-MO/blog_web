from blogMain.models import BlogPost
from .forms import BlogPostForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from blogMain.models import BlogCategory
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')

def detail(request, blog_id):
    return render(request, 'blog_detail.html')

# @login_required(login_url=reverse_lazy('blogAuth:blogAuth_login'))#django包含的登录装饰器，未登录用户访问会跳转到登录页面
@require_http_methods(['GET', 'POST'])
@login_required()
def public(request):
    
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'public.html', {'categories': categories})
    else:
        form = BlogPostForm(request.POST)
        print("11111111111111111111111111111111")
        if form.is_valid():
            
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            content = form.cleaned_data['content']

            BlogPost.objects.create(title=title, category_id=category, content=content, auther=request.user)

            print(title, category, content, request.user)
            return JsonResponse({'code': 200, 'message': 'success'})
        else:
            form_errors = form.errors.as_json()
            print(form_errors)
            return JsonResponse({'code': 400, 'message': 'error'})


from django.shortcuts import redirect
from blogMain.models import BlogPost
from .forms import BlogPostForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods ,require_POST,require_GET
from blogMain.models import BlogCategory
from django.http import JsonResponse
from blogMain.models import BlogComment
from django.db.models import Q


# Create your views here.


def index(request):
    return render(request, 'index.html')


def detail(request, blog_id):
    try:
        blog = BlogPost.objects.get(pk=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'blog not found'})
    
    return render(request, 'blog_detail.html', {'blog': blog})


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
            blog_id = BlogPost.objects.latest('id').id

            print(title, category, content, request.user)
            return JsonResponse({'code': 200, 'message': 'success', 'blog_id': blog_id})
        else:
            form_errors = form.errors.as_json()
            print(form_errors)
            return JsonResponse({'code': 400, 'message': 'error', 'form_errors': form_errors})

@require_POST
@login_required()
def comment(request):
    blog_id = request.POST.get('blog_id')
    print(blog_id)
    content = request.POST.get('content')
    if content != '':
        BlogComment.objects.create(post_id=blog_id, content=content, auther=request.user)
    return redirect(reverse('blogMain:blogMain_detail', kwargs={'blog_id': blog_id}))

@require_GET
def search(request):
    q = request.GET.get('q')
    blogs = BlogPost.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    print(blogs)
    return render(request, 'index.html', {'blogs': blogs})

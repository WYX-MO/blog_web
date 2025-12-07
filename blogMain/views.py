from re import S
from django.shortcuts import redirect
from blogMain.models import BlogPost,Star_table
from .forms import BlogPostForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods ,require_POST,require_GET
from blogMain.models import BlogCategory
from django.http import JsonResponse
from blogMain.models import BlogComment
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.http import HttpResponseNotFound
import os

# Create your views here.


def index(request):
    # 获取所有博客
    blogs = BlogPost.objects.all()
    # 初始化收藏的博客ID列表（兼容未登录）
    stars = []
    if request.user.is_authenticated:
        stars = Star_table.objects.filter(
            user_id=request.user.id
        ).values_list('blog_id', flat=True)
    for s in stars:
        s = int(s)
    print(stars)
    # # 为每个博客计算收藏总数
    # for blog in blogs:
    #     blog.star_count = Star_table.objects.filter(blog_id=blog.id).count()
    
    return render(request, 'index.html', {
        'blogs': blogs,
        'stars': stars
    })

def detail(request, blog_id):
    try:
        blog = BlogPost.objects.get(pk=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'blog not found'})
    stars = []
    if request.user.is_authenticated:
        stars = Star_table.objects.filter(
            user_id=request.user.id
        ).values_list('blog_id', flat=True)
    for s in stars:
        s = int(s)
    print(stars)
    return render(request, 'blog_detail.html', {'blog': blog, 'stars': stars})


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
    if q == 'user_stared_114':
        stars = Star_table.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
        blogs = BlogPost.objects.filter(id__in=stars).all()
    else:
        stars = []
        blogs = BlogPost.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    print(blogs)
    return render(request, 'index.html', {'blogs': blogs, 'stars': stars})

def decoy(request):
    return render (request, "decoy.html")


@require_POST
@login_required() 
def toggle_star(request):
    
    article_id = request.POST.get("article_id")
    if not article_id or not article_id.isdigit():  # 校验ID是否为有效数字
        return JsonResponse({
            "status": "error",
            "msg": "缺少或无效的文章ID"
        }, status=400)
    
    
    article = get_object_or_404(BlogPost, id=article_id)
    user = request.user

    try:
        
        has_starred = Star_table.objects.filter(
            user_id=user.id,
            blog_id=article.id
        ).exists()

        if has_starred:
            
            Star_table.objects.filter(user_id=user.id, blog_id=article.id).delete()
            new_btn_text = "收藏" 
            article.stars -= 1
            article.save()
        else:
            
            Star_table.objects.create(user_id=user.id, blog_id=article.id)
            new_btn_text = "取消收藏" 
            article.stars += 1
            article.save()
        print(article.id,article.stars,article.comments.count())
        # 4. 返回成功结果
        return JsonResponse({
            "status": "success",
            "new_btn_text": new_btn_text,
            "new_count": f"{article.comments.count()} 条评论 {article.stars} 个收藏"
        })
    
    except Exception as e:
        
        return JsonResponse({
            "status": "error",
            "msg": f"操作失败：{str(e)}"
        }, status=500)
    
def decoy(request):
    return render(request,'decoy.html')

def download_index(request):
    return render(request, 'download.html')

def download(request, filename):
    # 1. 拼接文件绝对路径
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'files')
    file_path = os.path.join(static_dir, filename)
    
    # 2. 验证文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return HttpResponseNotFound("文件不存在！")
    
    # 3. 打开文件（rb=二进制只读模式，支持所有文件类型）
    file = open(file_path, 'rb')
    
    # 4. 构建响应：指定文件类型（application/octet-stream 表示二进制文件，适配所有类型）
    response = FileResponse(file, content_type='application/octet-stream')
    
    # 5. 设置响应头：指定下载文件名（浏览器会自动识别）
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


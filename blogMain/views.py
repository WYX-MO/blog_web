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
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os

# Create your views here.
def hello(request):
    return render(request, 'newIndex.html')

def index(request):
    # 1. 获取所有博客并按发布时间倒序排序（推荐）
    blog_list = BlogPost.objects.all().order_by('-publicTime')
    # 2. 分页配置：每页显示6条（可根据需求调整）
    paginator = Paginator(blog_list, 6)
    page = request.GET.get('page', 1)  # 默认第一页

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    # 3. 收藏的博客ID列表（兼容未登录）
    stars = []
    if request.user.is_authenticated:
        stars = Star_table.objects.filter(
            user_id=request.user.id
        ).values_list('blog_id', flat=True)
    stars = [int(s) for s in stars]  # 转换为整数列表

    # 4. 分类数据（带文章数量）
    categories = BlogCategory.objects.annotate(blog_count=Count('blogpost'))

    return render(request, 'index.html', {
        'blogs': blogs,
        'stars': stars,
        'categories': categories,
        'paginator': paginator,  # 传递分页器供前端判断是否有下一页
    })

@require_GET
def load_more_blogs(request):
    """加载更多博客的接口，返回JSON数据"""
    try:
        # 1. 获取分页参数
        page = request.GET.get('page', 2)  # 默认加载第二页
        page = int(page)

        # 2. 查询博客并分页
        blog_list = BlogPost.objects.all().order_by('-publicTime')
        paginator = Paginator(blog_list, 6)  # 与index视图保持一致的每页数量

        # 3. 获取指定页数据
        blogs = paginator.page(page)

        # 4. 构造返回的博客数据（序列化）
        blog_data = []
        for blog in blogs:
            blog_data.append({
                'id': blog.id,
                'title': blog.title,
                'category_name': blog.category.name,
                'content': blog.content[:100],  # 与前端一致的截断
                'author_username': blog.auther.username,
                'author_id': blog.auther.id,
                'comments_count': blog.comments.count(),
                'stars_count': blog.stars,
                'publicTime': blog.publicTime.strftime('%Y-%m-%d %H:%M'),  # 格式化时间
                'detail_url': reverse('blogMain:blogMain_detail', args=[blog.id]),
            })

        # 5. 返回JSON响应
        return JsonResponse({
            'status': 'success',
            'blogs': blog_data,
            'has_next': blogs.has_next(),  # 是否有下一页
            'next_page': page + 1 if blogs.has_next() else None,  # 下一页页码
        })

    except PageNotAnInteger:
        return JsonResponse({'status': 'error', 'msg': '页码必须是整数'}, status=400)
    except EmptyPage:
        return JsonResponse({'status': 'error', 'msg': '没有更多数据了'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)
    


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
        blogs = BlogPost.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(category__name=q)).all()
    print(blogs)
    categories = BlogCategory.objects.annotate(blog_count=Count('blogpost'))
    return render(request, 'index.html', {'blogs': blogs, 'stars': stars, 'categories': categories})

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


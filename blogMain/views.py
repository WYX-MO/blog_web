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

# Create your views here.


def index(request):
    
    return render(request, 'index.html', {'blogs': BlogPost.objects.all()})


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

def decoy(request):
    return render (request, "decoy.html")

# @require_POST
# @login_required()
# def star(request, article_id):
#     print(article_id)
#     try:
#         blog = BlogPost.objects.get(pk=article_id)
#     except BlogPost.DoesNotExist:
#         return JsonResponse({'code': 404, 'message': 'blog not found'})
#     try:
#         Star_table.objects.create(user_id=request.user.id, blog_id=article_id)
#     except Star_table.DoesNotExist:
#         return JsonResponse({'code': 404, 'message': 'star failed'})
#     return JsonResponse({'code': 200, 'message': 'star success'})

# @require_POST
# @login_required()
# def toggle_star(request):

#     if request.method == "POST" :
#         article_id = request.POST.get("article_id")
#         article = get_object_or_404(BlogPost, id=article_id)
#         user = request.user

#         # 1. 查询/创建收藏记录
#         record, created = Star_table.objects.get_or_create(
#             user_id=user.id,
#             blog_id=article.id,
#         )

#         # 2. 切换收藏状态 + 确定按钮文字
#         if Star_table.objects.filter(user_id=user.id, blog_id=article.id).exists():
#             # 当前是“已收藏” → 改为“未收藏”，按钮文字返回“收藏”
#             record.delete()
#             Star_table.objects.filter(user_id=user.id, blog_id=article.id).delete()
#             new_btn_text = "收藏0"
#         else:
#             new_btn_text = "取消收藏"
#         print(new_btn_text)
#         # 3. 保存到数据库

#         # 4. 返回结果给前端
#         return JsonResponse({
#             "status": "success",
#             "new_btn_text": new_btn_text  # 核心：返回目标文字
#         })
    
#     return JsonResponse({"status": "error", "msg": "请求方式错误"}, status=400)

@require_POST  # 仅允许POST请求，无需再判断request.method == "POST"
@login_required(login_url="/login/")  # 未登录跳转到登录页（可选配置）
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
        else:
            
            Star_table.objects.create(user_id=user.id, blog_id=article.id)
            new_btn_text = "取消收藏" 

        # 4. 返回成功结果
        return JsonResponse({
            "status": "success",
            "new_btn_text": new_btn_text
        })
    
    except Exception as e:
        
        return JsonResponse({
            "status": "error",
            "msg": f"操作失败：{str(e)}"
        }, status=500)
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')

def detail(request, blog_id):
    return render(request, 'blog_detail.html')

# @login_required(login_url=reverse_lazy('blogAuth:blogAuth_login'))#django包含的登录装饰器，未登录用户访问会跳转到登录页面
@login_required()
def public(request):

    return render(request, 'public.html')


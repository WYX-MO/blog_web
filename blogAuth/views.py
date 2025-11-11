from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse  # 改用JsonResponse更便捷
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import string
import random
from .models import captcha as CaptchaModel
from .forms import RegisterForm

# 注册视图（支持GET和POST，POST返回JSON）
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 表单验证通过，创建用户
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogAuth:blogAuth_login'))
        else:
            # 提取错误信息返回给前端
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            return JsonResponse({
                'code': 400, 
                'msg': '表单验证失败', 
                'errors': errors
            })

# 登录视图（保持原样）
def login(request):
    return render(request, 'login.html')

# 发送验证码视图（修正URL映射和返回格式）
@require_http_methods(["GET"])
def send_email_vertify(request):  # 注意：函数名保持与URL映射一致
    email = request.GET.get('email', '').strip()
    if not email:
        return JsonResponse({'code': 400, 'msg': '请输入邮箱'})
    
    # 验证邮箱格式
    if not '@' in email or '.' not in email.split('@')[-1]:
        return JsonResponse({'code': 400, 'msg': '邮箱格式不正确'})
    
    # 检查邮箱是否已注册
    if User.objects.filter(email=email).exists():
        return JsonResponse({'code': 400, 'msg': '该邮箱已注册'})
    
    # 生成验证码并存储
    captcha = "".join(random.sample(string.digits, k=6))
    # 测试时固定验证码（正式环境删除）
    captcha = "123123"
    print(f"验证码：{captcha}")  # 开发环境调试用
    CaptchaModel.objects.update_or_create(email=email, defaults={'code': captcha})
    
    # 发送邮件
    try:
        send_mail(
            '博客注册验证码',
            f'您的注册验证码为：{captcha}，5分钟内有效，请勿泄露给他人。',
            '你的发件邮箱@qq.com',  # 替换为实际发件邮箱（在settings.py中配置的）
            [email],
            fail_silently=False,
        )
        return JsonResponse({'code': 200, 'msg': '验证码已发送'})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': f'发送失败：{str(e)}'})
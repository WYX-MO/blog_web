from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import json
import string
import random
from .models import captcha as CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                return HttpResponse(json.dumps({'code': 400, 'msg': 'username already exists'}), content_type='application/json')
            if User.objects.filter(email=email).exists():
                return HttpResponse(json.dumps({'code': 400, 'msg': 'email already exists'}), content_type='application/json')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogAuth:blogAuth_login'))
        else:
            print(form.errors)
            return redirect(reverse('blogAuth:blogAuth_register'))


def login(request):
    return render(request, 'login.html')

def send_email_vertify(request):
    email = request.GET.get('email')
    if email is None:
        return HttpResponse(json.dumps({'code': 400, 'msg': 'email is None'}), content_type='application/json')
    captcha = "".join(random.sample(string.digits,k = 6))
    captcha = "123123"  # for test
    print(captcha)
    CaptchaModel.objects.update_or_create(email=email, defaults={'code': captcha})
    try:
        send_mail(
            '博客注册验证码',
            f'您的注册验证码为：{captcha}，请勿泄露给他人，如非本人操作，请忽略本邮件。',
            None,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return HttpResponse(json.dumps({'code': 500, 'msg': 'send email failed'}), content_type='application/json')
    return HttpResponse(json.dumps({'code': 200, 'msg': 'success'}), content_type='application/json')

from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import json
import string
import random
from .models import captcha as CaptchaModel
# Create your views here.

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def send_email_vertify(request):
    email = request.GET.get('email')
    if email is None:
        return HttpResponse(json.dumps({'code': 400, 'msg': 'email is None'}), content_type='application/json')
    captcha = "".join(random.sample(string.digits,k = 6))
    print(captcha)
    CaptchaModel.objects.update_or_create(email=email, defaults={'code': captcha})
    send_mail(
        '博客注册验证码',
        f'您的注册验证码为：{captcha}，请勿泄露给他人，如非本人操作，请忽略本邮件。',
        None,
        [email],
        fail_silently=False,
    )
    return HttpResponse(json.dumps({'code': 200, 'msg': 'success'}), content_type='application/json')

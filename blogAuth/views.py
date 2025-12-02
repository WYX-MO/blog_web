
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import json
import string
import random
from .models import captcha as CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import login, logout

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
                return HttpResponse(json.dumps({'code': 400, 'msg': 'email already exists'}), content_type='application/json')
            if User.objects.filter(email=email).exists():
                return HttpResponse(json.dumps({'code': 400, 'msg': 'email already exists'}), content_type='application/json')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blogAuth:blogAuth_login'))
        else:
            print(form.errors)
            return redirect(reverse('blogAuth:blogAuth_register'))

@require_http_methods(["GET", "POST"])
def mylogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            
            if user and user.check_password(password):

                login(request, user)
                if remember is None:
                    remember = 0
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(60 * 60 * 24)
                request.session['user_id'] = user.id
                next_url = request.GET.get('next')
                print(next_url)
                if next_url is None:
                    next_url = reverse('blogMain:blogMain_index')
                return redirect(next_url)
            else:
                print('email or password is incorrect')
                return redirect(reverse('blogAuth:blogAuth_login'))
        else:
            print(form.errors)
            return redirect(reverse('blogAuth:blogAuth_login'))

@require_http_methods(["GET"])
def mylogout(request):
    logout(request)
    return redirect(reverse('blogAuth:blogAuth_login'))



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
            '验证码:',
            f'您的验证码为:{captcha}',
            "伟大的iizom <1739645729@qq.com>",
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return HttpResponse(json.dumps({'code': 500, 'msg': 'send email failed'}), content_type='application/json')
    return HttpResponse(json.dumps({'code': 200, 'msg': 'success'}), content_type='application/json')

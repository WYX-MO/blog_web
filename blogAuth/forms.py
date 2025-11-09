from django import forms
from django.contrib.auth.models import User
from .models import captcha as CaptchaModel

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, required=True,error_messages={'required': '用户名不能为空', 'max_length': '用户名过长', 'min_length': '用户名过短'})
    email = forms.EmailField(max_length=254, required=True,error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式不正确'})
    password = forms.CharField(max_length=20, min_length=4, required=True,error_messages={'required': '密码不能为空', 'max_length': '密码过长', 'min_length': '密码过短'})
    captcha = forms.CharField(max_length=6,min_length=6, required=True,error_messages={'required': '验证码不能为空', 'max_length': '验证码长度为6位', 'min_length': '验证码长度为6位'})
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self.add_error('email', '邮箱已存在')
            raise forms.ValidationError('邮箱已存在')
        return email
    
    def clean_captcha(self):
        email = self.cleaned_data.get('email')
        code = self.cleaned_data['captcha']
        captcha = CaptchaModel.objects.filter(email=email).first()
        if not captcha or captcha.code != code:
            raise forms.ValidationError('验证码错误')
        captcha.delete()
        return code

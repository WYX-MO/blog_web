from django.urls import path
from . import views

app_name = 'blogAuth'

urlpatterns = [
    path('login/', views.login, name='blogAuth_login'),
    path('register/', views.register, name='blogAuth_register'),
    path('send_email/', views.send_email_vertify, name='blogAuth_send_email_verify'),
]
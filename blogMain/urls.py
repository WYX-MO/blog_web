from django.urls import path

from . import views

app_name = 'blogMain'
urlpatterns = [
   path('index/', views.index, name='blogMain_index'),
]
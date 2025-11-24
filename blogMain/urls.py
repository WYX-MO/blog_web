from django.urls import path

from . import views

app_name = 'blogMain'

urlpatterns = [
   path('', views.index, name='blogMain_index'),
   path('detail/<int:blog_id>/', views.detail, name='blogMain_detail'),
   path('public/', views.public, name='blogMain_public'),
   path('comment/', views.comment, name='blogMain_comment'),
   path('search/', views.search, name='blogMain_search'),
   path('decoy/',views.decoy,name = "decoy"),
   path('toggle_star/', views.toggle_star, name='toggle_star'),
]
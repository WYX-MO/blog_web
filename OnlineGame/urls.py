# game/urls.py
from django.urls import path
from OnlineGame import views

app_name = 'OnlineGame'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.game_room, name='game_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('make-choice/', views.make_choice, name='make_choice'),
]
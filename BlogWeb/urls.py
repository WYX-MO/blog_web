"""
URL configuration for BlogWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from blogMain import views
from OnlineGame import views as game_views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('blog/', include('blogMain.urls')),
    path('auth/', include('blogAuth.urls')),
    # path('game/', include('OnlineGame.urls')),
    path('game/', game_views.index, name='game_index'),  # 游戏首页：http://127.0.0.1:8000/game/
    path('game/<str:room_name>/', game_views.game_room, name='game_room'),  # 游戏房间：http://127.0.0.1:8000/game/111/
    path('join-room/', game_views.join_room, name='join_room'),  # AJAX接口：/join-room/
    path('make-choice/', game_views.make_choice, name='make_choice'),  # AJAX接口：/make-choice/
    
    
]

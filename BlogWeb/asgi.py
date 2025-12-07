import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# 必须先初始化 Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlogWeb.settings')
django.setup()

# 导入 WebSocket 路由（初始化后导入，避免循环依赖）
from OnlineGame.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    # HTTP 请求走 Django 原生 ASGI
    "http": get_asgi_application(),
    # WebSocket 请求走 Channels
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
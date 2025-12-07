from django.urls import re_path
from . import consumers

# WebSocket 路由：匹配 ws/rps/房间名/
websocket_urlpatterns = [
    re_path(r'ws/rps/(?P<room_name>\w+)/$', consumers.RPSConsumer.as_asgi()),
]
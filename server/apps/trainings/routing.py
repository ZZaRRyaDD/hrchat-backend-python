from django.urls import path

from . import consumers


chat_websocket_urlpatterns = [
    path('ws/chat/<chat_uuid>/', consumers.ChatConsumer.as_asgi()),
]

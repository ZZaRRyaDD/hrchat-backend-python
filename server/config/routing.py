"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.common.middleware import JWTQueryParamAuthMiddleware
from apps.trainings.routing import chat_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

websocket_urlpatterns = chat_websocket_urlpatterns

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': JWTQueryParamAuthMiddleware(
    URLRouter(websocket_urlpatterns),
  ),
})

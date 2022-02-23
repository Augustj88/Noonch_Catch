"""
ASGI config for noonch_catch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter({ #채널즈 개발 서버에 연결이 구성될때 얘가 먼저 연결 타입을 확인
  "http": get_asgi_application(), #일반 HTTP이면 여기로 연결
  "websocket": AuthMiddlewareStack( #웹소캣 타입이면 여기로 연결. 현재 인증된 유저에 대한 참조를
      #연결의 scope에 추가.
        URLRouter( #이것은 url router에게 전달.
            chat.routing.websocket_urlpatterns #http경로를 확인해 적절한 컨슈머에게 연결해줌.
        )
    ),
})
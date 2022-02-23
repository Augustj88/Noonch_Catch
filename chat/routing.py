from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

#이제 chat 앱을 위한 라우팅 설정을 만들어 요청을 이 컨슈머로 전달해줘야함.

#대형 사이트등은 웹소켓 연결을 다른 일반적인 HTTP연결과 구분짓기 위해 웹 소캣용 경로에는 앞에 /ws/를 붙여준다.
#이를 통해 채널즈 픙로덕션 환경에 배포할때 설정을 쉽게 할 수있음.
#즉 1. 일반 http요청은 WSGI서버로 전달되고
#2. 웹소켓 요청은 ASGI서버로 전달해 처리하는 것이 가능.
#as_asgi()? ASGI 애플리케이션을 얻기 위해 호출된 것. 각 유저별 연결 처리하는 컨슈머 인스턴스를 만들어줌.
#이 메서드는 요청별로 장고 뷰 인스턴스를 만들어주는 as_view()와 유사.
# as_view? Any arguments passed to as_view() will override attributes set on the class,
#A similar overriding pattern can be used for the url attribute on RedirectView.
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer #동기적과는 다르게 WebsocketConsumer를 상속 받음.

class ChatConsumer(AsyncWebsocketConsumer):
    #connet: 참여할때마다 불러주는 함수
    #receive: 사람들이 메시지 보낼때마다 불러주는 함수 
    # #모든 연결을 accept하고, 클라이언트로부터 메시지를 receive하고, 동일한 client에게
    # #다시 이 메시지를 send해줌
    async def connect(self): #동기적과는 다르게 모든 메서드들이 그냥 def가 아니라 async def이다!
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name


        # Join room group
        await self.channel_layer.group_add( #입출력 작업을 수행하는 비동기 함수를 호출하기 위해 await가 사용
            self.room_group_name,
            self.channel_name
        )

        # 몇명 들어와있는지 찾는 부분!!!
        # self.count 에 몇명 들어와있는지가 기록!! #zcount: redis쪽에서 추가된 connection수를 가져오는 것 
        print(self.scope["headers"]) #cookie하면 닉네임을 찾을 수 있음  -> 입력된 값을 잡아서 내주기!
        async with self.channel_layer.connection(self.channel_layer.consistent_hash(self.channel_layer._group_key(self.room_group_name))) as connection:
            self.count = await connection.zcount(self.channel_layer._group_key(self.room_group_name)) #zcount: redis쪽에서 추가된 connection수를 가져오는 것 

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': 'admin',
                'message': f'{self.count} 명 입장하였습니다'
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        # -->
        # Send message to room group
        #동기적과는 에서는 메서드를 호출할때 async_to_sync가 필요했으나 채널레이어 상에서 메서드를 호출할 때async_to_sync가 더이상 필요하지 않음.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message ,
                'username' : username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))


#아래는 동기적 코드를 수행.
#동기적인 컨슈머는 장고 모델 접근과 같은 일반적인 동기적 입출력 함수들을 별다른 처리 없이 사용할 수 있어서 편리합니다.
# 하지만 비동기적인 컨슈머들은 요청을 처리할 때 별도의 쓰레드를 만들 필요가 없어 훨씬 우수한 성능을 자랑합니다.
# # chat/consumers.py
# import json
#
# from asgiref.sync import async_to_sync #채널 레이어를 사용하기 위해..
# from channels.generic.websocket import WebsocketConsumer
#
#
# #즉 유저가 메시지를 전송 -> 자바스크립트 함수는 웹 소캣을 통해 chatConsumer로 전송 -> chatConsumer는 메시지를 받아
# #-> 채팅방 이름에 해당하는 그룹으로 전파. 같은 그룹안에 있는 모든 chatConsumer는 그룹으로부터 메시지를 전달받아 -> 웹소켓을통해
# #자바스크립트로 이를 돌려주고 -> 채팅 로그에 메시지가 추가됨.
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         #웹소켓 연결을 컨슈머에게 전달한 chat/routing.py의 url route로부터 room_name을 얻는다
#         #모든 컨슈머는 자신의 연결에 대한 정보가 담긴 SCOPE을 갖음. -> 여기 안에는 모든 url route인자들과 인증된 유저정보가 들어있음.
#         self.room_group_name = 'chat_%s' % self.room_name
#         #채널즈 그룹명을 유저가 지정한 채팅방 이름에서 다른 처리 없이 직접 구성합니다.
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             #그룹에 들어감.
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()#웹소켓 연결을 accept함. 아래의 함수에는 없는데, 이뜻은 연결 요청을 거부하고 종료한다는 뜻.
#
#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             # 그룹을 떠남.
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data): # 클라이언트로부터 메시지를 receive하고
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             #그룹의 이벤트를 전송. event는 메서드명에 대응되는 type의 키를 갖고있음. 이벤트 받는 컨슈머는
#             #대응되는 메서드명의 메서드를 실행.
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#    # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer #동기적과는 다르게 WebsocketConsumer를 상속 받음.
from .models import Room
from channels.db import database_sync_to_async

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

        # 닉네임 찾기
        headers = self.scope["headers"][10][1].decode('utf-8')
        nick_index = headers.index('nickname')
        try:
            end_index = headers.index(';', nick_index)
            self.nick_name = headers[nick_index+9:end_index] #cookie하면 닉네임을 찾을 수 있음  -> 입력된 값을 잡아서 내주기!
        except:
            self.nick_name = headers[nick_index+9:] #cookie하면 닉네임을 찾을 수 있음  -> 입력된 값을 잡아서 내주기!

        # 몇명 들어와있는지 찾는 부분!!!
        # self.count 에 몇명 들어와있는지가 기록!! #zcount: redis쪽에서 추가된 connection수를 가져오는 것
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

        # db에다가 생성 (효율적인 방식은 아니지만.. 시간이 없으므로 이렇게 갑시다)
        await database_sync_to_async(Room.objects.create, thread_sensitive=True)(roomname=self.room_name, nickname=self.nick_name)

    async def disconnect(self, close_code):
        # db에다가 생성 (효율적인 방식은 아니지만.. 시간이 없으므로 이렇게 갑시다)
        user = await database_sync_to_async(Room.objects.get, thread_sensitive=True)(roomname=self.room_name, nickname=self.nick_name)
        await database_sync_to_async(user.delete)()
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
                'message': message,
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

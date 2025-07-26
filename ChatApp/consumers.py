import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received message: {data}")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': data
            }
        )

    async def send_message(self, event):
        data = event['message']
        print(f"Sending message: {data}")

        await self.create_message(data)

        await self.send(text_data=json.dumps({
            'message': data['message'],
            'username': data['username'],
        }))

    @database_sync_to_async
    def create_message(self, data):
        room = Room.objects.get(name=data['room_name'])  # you can wrap in try/except later
        new_message = Message(
            room=room,
            sender=data['username'],
            message=data['message']
        )
        new_message.save()
        return new_message

# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Room
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'message' in data:
            await self.handle_chat_message(data)
        elif 'delete' in data:
            await self.handle_message_deletion(data)

    async def handle_chat_message(self, data):
        message = data['message']
        username = data['username']
        room = data['room']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        deletable = data.get('deletable', True)  # Default to True if not provided

        await self.save_message(username, room, message, timestamp, deletable)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username,
                'room': room,
                'timestamp': timestamp,
                'deletable': deletable,
            }
        )

    async def handle_message_deletion(self, data):
        await self.delete_message(data['delete']['message_id'])

        # Broadcast a message indicating the deletion to all clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message_deleted',
                'message_id': data['delete']['message_id'],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'room': event['room'],
            'timestamp': event['timestamp'],
            'deletable': event['deletable'],
        }))

    async def chat_message_deleted(self, event):
        # Notify all clients that a message has been deleted
        await self.send(text_data=json.dumps({
            'message_deleted': event['message_id'],
        }))

    @sync_to_async
    def save_message(self, username, room, message, timestamp, deletable):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        # If timestamp is not provided, use the current time
        if not timestamp:
            timestamp = datetime.now()

        return Message.objects.create(user=user, room=room, content=message, timestamp=timestamp, deletable=deletable)

    @sync_to_async
    def delete_message(self, message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
        except Message.DoesNotExist:
            pass

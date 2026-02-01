import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import ChatMessage


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Optional: connection ack
        await self.send(text_data=json.dumps({
            "type": "connection",
            "status": "connected",
            "room": self.room_name,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Invalid JSON"
            }))
            return

        message = data.get('message')
        receiver = data.get('receiver', 'all')

        # Get sender from connection scope (requires AuthMiddlewareStack)
        sender_user = self.scope.get('user')
        if not sender_user or not getattr(sender_user, 'is_authenticated', False):
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Authentication required to send messages"
            }))
            return

        sender = getattr(sender_user, 'id', None)

        if not message:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Message cannot be empty"
            }))
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
            }
        )

        # Persist the message if receiver is a numeric id (direct message)
        try:
            # JSON numbers come in as int/float in Python; accept ints only
            if isinstance(receiver, int) and isinstance(sender, int):
                await self.save_message(sender, receiver, message)
        except Exception:
            # Don't fail the WebSocket if DB save fails; just log in server logs
            import logging
            logging.exception('Failed saving chat message')

        await self.send(text_data=json.dumps({
            "type": "ack",
            "message": "Message delivered"
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event['message'],
            "sender": event['sender'],
            "receiver": event['receiver'],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        """Create a ChatMessage instance linking to sender and receiver User ids.

        Returns the created ChatMessage or None if users don't exist.
        """
        try:
            sender = User.objects.get(pk=sender_id)
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return None

        return ChatMessage.objects.create(sender=sender, receiver=receiver, content=content)

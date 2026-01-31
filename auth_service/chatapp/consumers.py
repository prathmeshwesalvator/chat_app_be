import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
        sender = data.get('sender', 'anonymous')
        receiver = data.get('receiver', 'all')

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

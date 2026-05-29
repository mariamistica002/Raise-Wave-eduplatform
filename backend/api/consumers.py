import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        if self.user.institution_id:
            self.inst_group = f"institution_{self.user.institution_id}"
        else:
            self.inst_group = None

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        if self.inst_group:
            await self.channel_layer.group_add(self.inst_group, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'message': f'Welcome {self.user.get_full_name()}!'
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self, 'inst_group') and self.inst_group:
            await self.channel_layer.group_discard(self.inst_group, self.channel_name)

    async def receive(self, text_data):
        # Ping-pong keep alive
        data = json.loads(text_data)
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type':    'notification',
            'title':   event.get('title', ''),
            'message': event.get('message', ''),
            'priority':event.get('priority', 'medium'),
        }))

    async def notice_created(self, event):
        await self.send(text_data=json.dumps({
            'type':    'notice',
            'notice':  event.get('notice', {}),
        }))

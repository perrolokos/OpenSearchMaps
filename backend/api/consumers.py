from channels.generic.websocket import AsyncJsonWebsocketConsumer


class KnowledgeMapConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.map_id = self.scope['url_route']['kwargs']['map_id']
        self.group_name = f"map_{self.map_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.group_name, {"type": "broadcast", "content": content}
        )

    async def broadcast(self, event):
        await self.send_json(event["content"])

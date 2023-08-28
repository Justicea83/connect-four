"""
Game consumers.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('CHANNEL NAME')
        print(self.channel_name)
        self.room_group_name = 'game'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('INCOMING ---->')
        print(text_data_json)
        action = text_data_json["action"]
        payload = text_data_json["payload"]

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": 'game_event',
                "action": action,
                "payload": payload,
                "user": self.scope['user']
            }
        )

    async def game_event(self, event):
        user = event['user']

        action = event['action']

        if action == 'action.play':
            # TODO save to db
            await self.send(
                text_data=json.dumps({
                    "action": event['action'],
                    "payload": event["payload"],
                    "user": event["user"].pk,
                })
            )

        if action == 'action.reset':
            # TODO reset the game
            await self.send(
                text_data=json.dumps({
                    "action": event['action'],
                    "user": event["user"].pk,
                })
            )

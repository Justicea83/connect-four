"""
Game consumers.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Game, GameAction
from channels.db import database_sync_to_async


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

    @database_sync_to_async
    def get_default_game(self) -> Game:
        return Game.objects.first()

    @database_sync_to_async
    def create_game_action(self, user, game, event):
        try:
            latest_record = GameAction.objects.latest('id')
            if latest_record.player != user:
                GameAction.objects.create(player=user, game=game, action=event["payload"])

        except GameAction.DoesNotExist:
            GameAction.objects.create(player=user, game=game, action=event["payload"])

    @database_sync_to_async
    def reset_game(self, game: Game):
        game.winner = None
        game.is_complete = False
        game.game_actions.all().delete()
        game.save()

    async def game_event(self, event):
        user = event['user']

        # For simplicity, we will use a single game model
        game = await self.get_default_game()

        action = event['action']

        if action == 'action.play':
            await self.send(
                text_data=json.dumps({
                    "action": event['action'],
                    "payload": event["payload"],
                    "user": event["user"].pk,
                })
            )
            await self.create_game_action(user=user, game=game, event=event)

        if action == 'action.reset':
            await self.send(
                text_data=json.dumps({
                    "action": event['action'],
                    "user": event["user"].pk,
                })
            )
            await self.reset_game(game)

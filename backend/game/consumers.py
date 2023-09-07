"""
Game consumers.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Game, GameAction
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import random


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'game'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
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
    def get_user_by_id(self, id) -> Game:
        return get_user_model().objects.get(id=id)

    @database_sync_to_async
    def create_game_action(self, user, game, event):
        try:
            latest_record = GameAction.objects.latest('id')
            if latest_record.player != user:
                GameAction.objects.create(player=user, game=game, action=event["payload"])

        except GameAction.DoesNotExist:
            GameAction.objects.create(player=user, game=game, action=event["payload"])

    async def bot_play(self, game):
        bot_id = 1
        user = await self.get_user_by_id(bot_id)
        direction = random.choice(['L', 'R'])
        row = random.choice([0, 1, 2, 3, 4, 5, 6])
        col = 0

        if direction == 'L':
            col = 0
        elif direction == 'R':
            col = 6

        action = f"{str(row)},{str(col)},{direction}"
        await self.create_game_action(user, game, {"payload": action})
        await self.send(
            text_data=json.dumps({
                "action": 'action.play',
                "payload": action,
                "user": bot_id,
            })
        )

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
            await self.bot_play(game)

        if action == 'action.reset':
            await self.send(
                text_data=json.dumps({
                    "action": event['action'],
                    "user": event["user"].pk,
                })
            )
            await self.reset_game(game)

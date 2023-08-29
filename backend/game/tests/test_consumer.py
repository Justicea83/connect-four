"""
Test the game consumer.
"""
import json
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from core.models import Game, User, GameAction
from game.consumers import GameConsumer
from game.mocks import MockWebsocketCommunicator
from channels.db import database_sync_to_async

ACTION_PLAY = 'action.play'
ACTION_RESET = 'action.reset'


@database_sync_to_async
def create_user(username='Adams', password='testpass123'):
    """Creates and return a new user."""
    return get_user_model().objects.create_user(username, password)


@database_sync_to_async
def count_game_actions():
    return GameAction.objects.count()


@database_sync_to_async
def create_game(
        player_one,
        player_two,
        **params
):
    """Creates and return a sample game."""
    defaults = {
        'player_one': player_one,
        'player_two': player_two
    }
    defaults.update(params)

    game: Game = Game.objects.create(**defaults)
    return game


class GameConsumerTest(TransactionTestCase):

    async def test_game_action(self):
        # Let's assume having 2 players
        player_one = await create_user(username='Gamer1')
        player_two = await create_user(username='Gamer2')

        previous_game_action_count = await count_game_actions()

        # Participate in a game
        await create_game(player_one=player_one, player_two=player_two)

        # If player_one makes an action
        communicator = MockWebsocketCommunicator(GameConsumer.as_asgi(), "/ws/game/", player_one)
        connected, subprotocol = await communicator.connect()
        await communicator.send_json_to({
            "action": ACTION_PLAY,
            "payload": "0,0,R"
        })
        message = json.loads(await communicator.receive_from())
        self.assertEqual(message['action'], ACTION_PLAY)
        self.assertEqual(message['user'], player_one.pk)
        assert connected
        self.assertEqual(previous_game_action_count + 1, await count_game_actions())
        await communicator.disconnect()

        # If player_two makes an action
        communicator = MockWebsocketCommunicator(GameConsumer.as_asgi(), "/ws/game/", player_two)
        connected, subprotocol = await communicator.connect()
        await communicator.send_json_to({
            "action": ACTION_PLAY,
            "payload": "1,0,R"
        })
        message = json.loads(await communicator.receive_from())
        self.assertEqual(message['action'], ACTION_PLAY)
        self.assertEqual(message['user'], player_two.pk)
        assert connected
        self.assertEqual(previous_game_action_count + 2, await count_game_actions())
        await communicator.disconnect()

    async def test_game_reset(self):
        # Let's assume having 2 players
        player_one = await create_user(username='Gamer1')
        player_two = await create_user(username='Gamer2')

        # Participate in a game
        game: Game = await create_game(
            player_one=player_one,
            player_two=player_two,
            is_complete=True,
            winner=player_one
        )

        # If player_two makes an action
        communicator = MockWebsocketCommunicator(GameConsumer.as_asgi(), "/ws/game/", player_one)
        connected, _ = await communicator.connect()
        await communicator.send_json_to({
            "action": ACTION_RESET,
            "payload": ""
        })
        message = json.loads(await communicator.receive_from())
        self.assertEqual(message['action'], ACTION_RESET)
        self.assertEqual(message['user'], player_one.pk)
        assert connected
        await database_sync_to_async(game.refresh_from_db)()
        self.assertFalse(game.is_complete)
        self.assertIsNone(game.winner)
        await communicator.disconnect()

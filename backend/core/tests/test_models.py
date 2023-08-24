"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User, Game, GameAction


def create_user(username='mike', password='testpass123'):
    """Creates and return a new user."""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_username_successful(self):
        username = 'james'
        password = 'testpass123'
        user: User = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_username_raises_error(self):
        """Test that creating a user without a username raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_game(self):
        """Test creating a game is successful."""
        player_one = create_user()
        player_two = create_user(username='Jamie')

        game: Game = Game.objects.create(
            player_one=player_one,
            player_two=player_two
        )

        self.assertEqual(str(game), f"{player_one.name}&{player_two.name}")

    def test_create_game_action(self):
        """Test creating an action in a game"""
        player = create_user()

        gameAction: GameAction = GameAction.objects.create(
            action='(2,R)',
            player=player
        )
        self.assertEqual(str(gameAction), f"{player.name}:{gameAction.action}")

"""
Test for game APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Game, User
from game.serializers import GameSerializer, GameDetailSerializer

GAMES_URL = reverse('game:game-list')
GAME_ACTIONS_URL = reverse('game:gameaction-list')


def detail_url(game_id):
    """Create and return a recipe detail URL"""
    return reverse('game:game-detail', args=[game_id])


def create_user(username='Adams', password='testpass123') -> User:
    """Creates and return a new user."""
    return get_user_model().objects.create_user(username, password)


def create_game(
        player_one,
        player_two,
        **params
) -> Game:
    """Creates and return a sample game."""
    defaults = {
        'player_one': player_one,
        'player_two': player_two
    }
    defaults.update(params)

    game: Game = Game.objects.create(**defaults)
    return game


class PublicGameAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(GAMES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGameAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            username='John'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_game(self):
        """Test retrieve recipes."""
        create_game(
            player_one=create_user(username='Gamer1'),
            player_two=self.user
        )
        create_game(
            player_one=create_user(username='Gamer3'),
            player_two=self.user
        )

        res = self.client.get(GAMES_URL)

        games = Game.objects.all().order_by('-id')
        serializer = GameSerializer(games, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_game_detail(self):
        """Test get game detail."""
        game: Game = create_game(
            player_one=create_user(username='Gamer1'),
            player_two=self.user
        )

        url = detail_url(game.pk)
        res = self.client.get(url)

        serializer = GameDetailSerializer(game)
        self.assertEqual(res.data, serializer.data)

    def test_create_game(self):
        """Test creating a game."""
        player_two = create_user(username='Gamer1')
        payload = {
            'player_one': self.user.pk,
            'player_two': player_two.pk
        }

        res = self.client.post(GAMES_URL, payload)
        game: Game = Game.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(game.player_one.pk, payload['player_one'])
        self.assertEqual(game.player_two.pk, payload['player_two'])

    def test_update_game(self):
        """Test updating a game."""
        player_two = create_user(username='Gamer1')

        game: Game = create_game(
            player_one=player_two,
            player_two=self.user
        )

        self.assertIsNone(game.winner)
        self.assertEqual(game.is_complete, False)

        url = detail_url(game.pk)

        res = self.client.patch(url, {
            'winner': player_two.pk,
            'is_complete': True
        })

        game.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(game.winner.pk, player_two.pk)
        self.assertEqual(game.is_complete, True)

    def test_create_game_action(self):
        """Test creating an action on a game."""
        player_two = create_user(username='Gamer1')

        game: Game = create_game(
            player_one=player_two,
            player_two=self.user
        )

        res1 = self.client.post(GAME_ACTIONS_URL, {
            'action': '(1,L)',
            'game': game.pk
        })

        res2 = self.client.post(GAME_ACTIONS_URL, {
            'action': '(2,L)',
            'game': game.pk
        })

        gameDetail = Game.objects.get(id=game.pk)
        serializer = GameDetailSerializer(gameDetail)

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(serializer.data['game_actions']), 2)

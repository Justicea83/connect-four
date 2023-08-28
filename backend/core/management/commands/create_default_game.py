"""
Django command to create default game for player one and two.
"""
from django.core.management import BaseCommand
from core.models import User, Game


class Command(BaseCommand):
    def handle(self, *args, **options):
        player_one = User.objects.get(username='frank')
        player_two = User.objects.get(username='james')

        game_exists = Game.objects.filter(player_one=player_one, player_two=player_two).exists()

        if not game_exists:
            Game.objects.create(player_one=player_one, player_two=player_two)

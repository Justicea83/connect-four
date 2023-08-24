"""Serializers for recipe API."""
from rest_framework import serializers

from core.models import GameAction, Game


class GameActionSerializer(serializers.ModelSerializer):
    """Serializer for game action"""

    class Meta:
        model = GameAction
        fields = ['action', 'game', 'id']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a game action."""

        auth_user = self.context['request'].user
        game: Game = Game.objects.get(pk=validated_data['game'].id)

        if game is not None:
            validated_data['player'] = auth_user
            game_action = GameAction.objects.create(**validated_data)
            return game_action
        return None


class GameSerializer(serializers.ModelSerializer):
    """Serializer for game."""

    class Meta:
        model = Game
        fields = ['id', 'player_one', 'player_two', 'winner', 'is_complete']
        read_only_fields = ['id', 'game_actions', 'winner', 'is_complete']
        extra_kwargs = {
            'player_one': {'required': 'True'},
            'player_two': {'required': 'True'},
        }


class GameDetailSerializer(GameSerializer):
    """Serializer for game detail view."""

    class Meta(GameSerializer.Meta):
        fields = GameSerializer.Meta.fields + ['game_actions']

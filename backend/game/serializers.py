"""Serializers for recipe API."""
from rest_framework import serializers

from core.models import GameAction, Game


class GameActionSerializer(serializers.ModelSerializer):
    """Serializer for game action"""

    class Meta:
        model = GameAction
        fields = ['action', 'game', 'id', 'player']
        read_only_fields = ['id', 'player']

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
        read_only_fields = ['id', 'winner', 'is_complete']
        extra_kwargs = {
            'player_one': {'required': 'True'},
            'player_two': {'required': 'True'},
        }


class GameDetailSerializer(GameSerializer):
    """Serializer for game detail view."""
    game_actions = serializers.SerializerMethodField()

    class Meta(GameSerializer.Meta):
        fields = GameSerializer.Meta.fields + ['game_actions']

    def get_game_actions(self, instance):
        actions = instance.game_actions.all().order_by('id')
        return GameActionSerializer(actions, many=True).data


class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['winner', 'is_complete']


class GameResetSerializer(serializers.ModelSerializer):
    """Serializer for game reset."""

    class Meta:
        model = Game
        fields = ['id']
        read_only_fields = ['id', 'winner', 'is_complete']

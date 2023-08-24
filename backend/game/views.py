from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Game, GameAction
from game import serializers


# Create your views here.
class GameViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """View to manage games."""
    serializer_class = serializers.GameDetailSerializer
    queryset = Game.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve games for authenticated user."""
        return self.queryset.filter(
            Q(player_one=self.request.user) | Q(player_two=self.request.user)
        ).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.GameSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return serializers.GameUpdateSerializer
        elif self.action == 'reset_game':
            return serializers.GameResetSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='reset', url_name='reset')
    def reset_game(self, request, pk=None):
        game: Game = self.get_object()

        game.winner = None
        game.is_complete = False
        game.game_actions.clear()

        """Reset the game."""
        serializer = self.get_serializer(game, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameActionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """View to manage game actions."""
    serializer_class = serializers.GameActionSerializer
    queryset = GameAction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-id')

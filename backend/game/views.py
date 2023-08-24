from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from core.models import Game, GameAction
from game import serializers


# Create your views here.
class GameViewSet(
    mixins.RetrieveModelMixin,
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

        return self.serializer_class


class GameActionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """View to manage game actions."""
    serializer_class = serializers.GameActionSerializer
    queryset = GameAction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

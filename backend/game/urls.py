"""
URL mappings for the game app.
"""

from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from game import views

router = DefaultRouter()
router.register('games', views.GameViewSet)
router.register('actions', views.GameActionViewSet)

app_name = 'game'

urlpatterns = [
    path('', include(router.urls))
]

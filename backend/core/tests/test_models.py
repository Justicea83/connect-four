"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import User


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

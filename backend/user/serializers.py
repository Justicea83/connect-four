"""
Serializers for the user API view
"""
from django.contrib.auth import (
    authenticate
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

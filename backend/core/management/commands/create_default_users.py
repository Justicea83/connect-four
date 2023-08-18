"""
Django command to create default users for the application.
"""
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        default_password = 'secret'
        default_users = [
            {
                'username': 'frank',
                'name': 'Frank',
            },
            {
                'username': 'james',
                'name': 'James',
            },
        ]
        for user in default_users:
            user_exists = User.objects.filter(username=user['username']).exists()
            if not user_exists:
                get_user_model().objects.create_user(**user, password=default_password)

        admin_exists = User.objects.filter(username='admin').exists()
        if not admin_exists:
            get_user_model().objects.create_superuser(username='admin', name='admin', password=default_password)

        self.stdout.write(self.style.SUCCESS('Default users setup complete!'))

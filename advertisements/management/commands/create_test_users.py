from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
import os


class Command(BaseCommand):
    help = 'Creates test users and saves their tokens to http-client environment file ("http-client.env.json")'

    def handle(self, *args, **options):
        usernames = ['user1', 'user2', 'user3']
        password = 'test_password'
        admin_username = 'admin1'
        admin_password = 'admin_password'  # Change this to a secure password

        env_file = 'http-client.env.json'
        if os.path.exists(env_file):
            with open(env_file, 'r') as file:
                data = json.load(file)
        else:
            data = {}

        for i, username in enumerate(usernames, start=1):
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()

            token, _ = Token.objects.get_or_create(user=user)
            data['dev'][f'token{i}'] = str(token.key)

        # Add the admin user
        admin_user, created = User.objects.get_or_create(username=admin_username, is_staff=True)
        if created:
            admin_user.set_password(admin_password)
            admin_user.save()

        admin_token, _ = Token.objects.get_or_create(user=admin_user)
        data['dev']['adminToken'] = str(admin_token.key)

        with open(env_file, 'w') as file:
            json.dump(data, file, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully created users and saved tokens to "http-client.env.json"'))

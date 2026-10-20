import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create a Render superuser once using environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not any((username, email, password)):
            self.stdout.write('Superuser bootstrap skipped; no credentials configured.')
            return

        if not all((username, email, password)):
            raise CommandError(
                'Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, '
                'and DJANGO_SUPERUSER_PASSWORD together.'
            )

        User = get_user_model()
        user = User.objects.filter(**{User.USERNAME_FIELD: username}).first()

        if user is not None:
            if not user.is_superuser:
                raise CommandError(
                    f'User {username!r} already exists but is not a superuser.'
                )
            self.stdout.write(f'Superuser {username!r} already exists; no changes made.')
            return

        User.objects.create_superuser(
            **{
                User.USERNAME_FIELD: username,
                'email': email,
                'password': password,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser {username!r} created.'))

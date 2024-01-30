from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from allauth.account.admin import EmailAddress


def fill_user():
    password = 'qqq'
    user = User.objects.create(
        username='testuser1',
        email='veha1337@gmail.com',
        password=make_password(password)

    )
    user.save()
    EmailAddress.objects.create(user=user, email=user.email, verified=True)


class Command(BaseCommand):
    help = "Create test user."

    def handle(self, *args, **options):
        fill_user()
        self.stdout.write(
            self.style.SUCCESS('create testuser.')
        )



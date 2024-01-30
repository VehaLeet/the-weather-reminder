from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in

from core.models import create_task


@receiver(user_logged_in)
def create_task_on_user_signup(sender, request, user, **kwargs):
    create_task(user)

import json
from django.utils import timezone
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.db import models, connection
from django_celery_beat.models import IntervalSchedule, PeriodicTask




class Subscription(models.Model):

    class Period(models.IntegerChoices):
        ONE = 1
        THREE = 3
        SIX = 6
        TWELVE = 12

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    period_notifications = models.IntegerField(choices=Period.choices)
    date_of_subscription = models.DateTimeField(auto_now_add=True)
    last_notification_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} has a subscription since {self.date_of_subscription} ' \
               f'with period of notifications - {self.period_notifications} hours.'


class CityInSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


def create_task(user):
    task_name = f'Send email to {user.email}'
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS
    )
    task = PeriodicTask.objects.create(
        name=task_name,
        task='send_email_task',
        interval=schedule,
        args=json.dumps([user.id]),
        start_time=timezone.now()
    )
    task.save()
    return


def edit_task(user, interval):
    task_name = f'Send email to {user.email}'
    existing_task = PeriodicTask.objects.filter(name=task_name).first()
    existing_task.interval.every = interval
    existing_task.interval.save()
    existing_task.save()
    return


def delete_task(subscription):
    task_name = f'Send email to {subscription.user.email} (subscription {subscription.id})'
    existing_task = PeriodicTask.objects.filter(name=task_name).first()
    existing_task.delete()
    return




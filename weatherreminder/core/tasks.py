import itertools
from datetime import timedelta
import requests
from celery import shared_task, chain, group
from celery.result import AsyncResult, allow_join_result
from celery.exceptions import TimeoutError
from weatherreminder.settings import OPEN_WEATHER_API_URL, OPEN_WEATHER_API_KEY, CACHES
from .models import Subscription, CityInSubscription
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.utils import timezone
from django_celery_beat.models import PeriodicTask
from redlock import MultipleRedlockException, Redlock


def get_weather(city_name):
    url = OPEN_WEATHER_API_URL + f'?q={city_name}&units=metric&appid={OPEN_WEATHER_API_KEY}'
    data = requests.get(url).json()
    weather_data = {
        'city': data['name'],
        'temperature': f"{data['main']['temp']}°C",
        'feels like': f"{data['main']['feels_like']}°C",
        'description': data['weather'][0]['description'],
        'wind speed': f'{data["wind"]["speed"]} m/s',
    }
    return weather_data


@shared_task(name="get_cached_weather", autoretry_for=(MultipleRedlockException, ), retry_kwargs={'max_retries': 5})
def get_cached_weather(city_name):
    lock_manager = Redlock([ CACHES['default']['LOCATION'] ])

    lock_name = f'{city_name}'
    lock = lock_manager.lock(lock_name, 10)
    try:
        if lock:
            print(f"Lock acquired for {lock_name}")
            cached_weather = cache.get(city_name)
            if cached_weather is not None:
                return cached_weather

            weather_data = get_weather(city_name)
            cache.set(city_name, weather_data, timeout=60 * 60)  # Cache for 1 hour
            return weather_data
        else:
            print(f"Failed to acquire lock for {lock_name}")
            return None  # or some default value
    finally:
        if lock:
            lock_manager.unlock(lock)

def notification_time(subscription):
    current_time = timezone.now()
    last_notification_time = subscription.last_notification_time

    if last_notification_time is None:
        subscription.last_notification_time = current_time
        last_notification_time = subscription.last_notification_time
        subscription.save()

    time_difference = current_time - last_notification_time + timedelta(seconds=1)
    time_difference_in_minutes = time_difference.total_seconds() // 60

    if time_difference_in_minutes >= subscription.period_notifications:
        subscription.last_notification_time = current_time
        subscription.save()
        return True
    return False


@shared_task(name="send_email_task")
def send_email_task(user_id):
    user = User.objects.get(id=user_id)
    user_subscriptions = Subscription.objects.filter(user=user).all()

    subtasks = []
    for subscription in user_subscriptions:
        if notification_time(subscription):
            cities = subscription.cities.all()
            subtasks.extend([get_cached_weather.s(city.name) for city in cities])

    tasks_group = group(*subtasks)
    tasks_result = tasks_group.apply_async()

    with allow_join_result():
        weathers = tasks_result.get()
        if weathers:
            html_content = ''
            for weather in weathers:
                html_content += f'''<p>
                                        <strong>{weather["city"]}</strong><br>
                                        Temperature {weather["temperature"]}<br>
                                        Feels like {weather["feels like"]}<br>
                                        {weather["description"]}<br>
                                        Wind speed {weather["wind speed"]}<br>
                                    </p>'''
            message = EmailMessage('Weather notification', html_content, to=[user.email])
            message.content_subtype = 'html'
            if message.send():
                print("Message was sent.")
            else:
                print("Message didn't send.")
            return



import requests
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weatherreminder.settings import OPEN_WEATHER_API_URL, OPEN_WEATHER_API_KEY
from .models import Subscription, CityInSubscription, create_task, edit_task, delete_task
from .serializers import SubscriptionSerializer, CityInSubscriptionSerializer
from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from django.shortcuts import get_object_or_404


from .tasks import get_weather, get_cached_weather


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def check_existing_city(city_name):
    url = OPEN_WEATHER_API_URL + f'?q={city_name}&appid={OPEN_WEATHER_API_KEY}'
    r = requests.get(url)
    return r.status_code != 200


def homepage(request):
    tokens = get_tokens_for_user(request.user)
    return render(request=request,
                  template_name='core/home.html',
                  context={
                      "refresh": tokens['refresh'],
                      "access": tokens['access'],
                  }
                  )


class MySubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user).all()
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)

    def post(self, request):
        new_subscription = Subscription.objects.create(
            user=request.user,
            period_notifications=request.data["period_notifications"]
        )
        new_subscription.save()
        serializer = SubscriptionSerializer(new_subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request):
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            subscription.delete()
        return Response("Subscriptions has been deleted")


class MySubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        subscription = Subscription.objects.filter(pk=pk).first()
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)


    def put(self, request, pk):
        subscription = Subscription.objects.filter(pk=pk).first()
        subscription.period_notifications = request.data["period_notifications"]
        subscription.save()
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def delete(self, request, pk):
        subscription = Subscription.objects.filter(pk=pk).first()
        subscription.delete()
        return Response("Subscription has been deleted")


class MyCitiesListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CityInSubscriptionSerializer

    def get_queryset(self):
        subscription_pk = self.kwargs['pk']
        subscription = Subscription.objects.get(pk=subscription_pk, user=self.request.user)
        return CityInSubscription.objects.filter(subscription=subscription)

    def create(self, request, *args, **kwargs):
        input_city = request.data['name']
        subscription_pk = self.kwargs['pk']
        subscription = Subscription.objects.get(pk=subscription_pk, user=self.request.user)
        existing_city = CityInSubscription.objects.filter(subscription=subscription, name=input_city)
        if existing_city:
            return Response("City already added in your subscription")
        if check_existing_city(input_city):
            return Response("City doesn't exist")
        new_city = CityInSubscription.objects.create(
            subscription=subscription,
            name=input_city,
        )
        new_city.save()
        serializer = CityInSubscriptionSerializer(new_city)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetWeatherView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        subscription = Subscription.objects.get(pk=pk, user=request.user)
        response_get_weather = []
        for city in subscription.cities.all():
            response_get_weather.append(get_cached_weather(city.name))
        return Response(response_get_weather)


class GetWeatherOneCityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, city_name):
        subscription = Subscription.objects.get(pk=pk, user=request.user)
        city = CityInSubscription.objects.filter(subscription=subscription, name=city_name).first()

        return Response(get_cached_weather(city.name))

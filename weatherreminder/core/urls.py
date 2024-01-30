from django.urls import path
from . import views
from .views import (
    MySubscriptionsView, MySubscriptionView,
    MyCitiesListView, GetWeatherView, GetWeatherOneCityView)


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('api/subscription/', MySubscriptionsView.as_view(), name='subscription'),
    path('api/subscription/<pk>/', MySubscriptionView.as_view(), name='subscription'),
    path('api/subscription/<pk>/cities/', MyCitiesListView.as_view(), name='cities'),
    path('api/subscription/<pk>/get_weather/', GetWeatherView.as_view(), name='get_weather'),
    path('api/subscription/<pk>/get_weather/<city_name>/', GetWeatherOneCityView.as_view(), name='get_weather_one'),
]

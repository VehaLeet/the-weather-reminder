from django.contrib import admin

from .models import Subscription, CityInSubscription


admin.site.register(Subscription)
admin.site.register(CityInSubscription)

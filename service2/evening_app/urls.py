from django.urls import path
from .views import GoodEveningView, health_check

urlpatterns = [
    path('', health_check, name='health_check'),
    path('evening/', GoodEveningView.as_view(), name='good_evening'),
]

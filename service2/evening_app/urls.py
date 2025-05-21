from django.urls import path
from .views import GoodEveningView, health_check

urlpatterns = [
    path('evening/', GoodEveningView.as_view(), name='good_evening'),
]

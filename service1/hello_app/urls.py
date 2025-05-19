from django.urls import path
from .views import HelloWorldView, health_check

urlpatterns = [
    path('', health_check, name='health_check'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
]

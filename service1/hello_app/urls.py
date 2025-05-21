from django.urls import path
from .views import HelloWorldView, health_check

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
]

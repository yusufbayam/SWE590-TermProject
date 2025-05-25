from django.urls import path
from .views import HelloWorldView, health_check, NegativeImageProxyView

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('negative-image/', NegativeImageProxyView.as_view(), name='negative_image_proxy'),
]

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

# Create your views here.

class HelloWorldView(APIView):
    def get(self, request):
        input_text = request.query_params.get('input', 'Stranger')
        return Response({
            'message': f'Hello World, {input_text}'
        })

def health_check(request):
    """Health check endpoint for GKE Ingress."""
    return HttpResponse("OK", status=200)

def hello_view(request):
    return JsonResponse({"message": "Hello from Service 1!"})

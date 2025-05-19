from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.

class GoodEveningView(APIView):
    def get(self, request):
        input_text = request.query_params.get('input', 'Stranger')
        return Response({
            'message': f'Good evening, {input_text}'
        })

def health_check(request):
    return HttpResponse("OK", status=200)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import os
import json
import traceback
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

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

@method_decorator(csrf_exempt, name='dispatch')
class NegativeImageProxyView(APIView):
    def post(self, request):
        # Get the file from the request
        image_file = request.FILES.get('file')
        if not image_file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        # Get the ID token from the request - now optional
        id_token = request.POST.get('id_token')
        
        try:
            # Prepare to call the Cloud Function
            function_url = 'https://us-central1-white-site-459410-c0.cloudfunctions.net/negative-image-function'
            
            # First try to call the Cloud Function directly without authentication
            # This is the primary method now that the function is public
            try:
                print("Calling Cloud Function without authentication...")
                files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
                response = requests.post(function_url, files=files)
                
                if response.status_code == 200:
                    # Return the image as a response
                    django_response = HttpResponse(response.content, content_type='image/png')
                    django_response['Content-Disposition'] = 'attachment; filename="negative.png"'
                    return django_response
                else:
                    print(f"Direct call failed with status {response.status_code}")
                    # If direct call fails and we have a token, try with authentication
            except Exception as direct_call_error:
                print(f"Direct call error: {str(direct_call_error)}")
                # Continue with authentication attempts if we have a token
            
            # Only try with the user's ID token if provided
            if id_token:
                try:
                    # Verify the ID token
                    try:
                        # Specify the CLIENT_ID from your Google OAuth credentials
                        client_id = '790253395116-3tuj7t3amf29guokqj406m5r3i39t0nd.apps.googleusercontent.com'
                        idinfo = google_id_token.verify_oauth2_token(
                            id_token, google_requests.Request(), client_id)
                        
                        # Check if the token is valid
                        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                            print("Invalid token issuer")
                            # Continue with other methods instead of returning error
                        else:
                            # Log the authenticated user
                            user_email = idinfo['email']
                            print(f"Authenticated user: {user_email}")
                            
                            # Try with the user's ID token
                            print("Trying with user's ID token...")
                            files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
                            headers = {'Authorization': f'Bearer {id_token}'}
                            response = requests.post(function_url, files=files, headers=headers)
                            
                            if response.status_code == 200:
                                # Return the image as a response
                                django_response = HttpResponse(response.content, content_type='image/png')
                                django_response['Content-Disposition'] = 'attachment; filename="negative.png"'
                                return django_response
                            else:
                                print(f"User token call failed with status {response.status_code}")
                                # If user token call fails, try with service account
                    except ValueError as e:
                        # Invalid token
                        print(f"Token verification error: {str(e)}")
                        # Continue with other methods instead of returning error
                except Exception as user_token_error:
                    print(f"User token error: {str(user_token_error)}")
                    # Continue with service account attempt
            
            # Try with service account if available
            credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path and os.path.exists(credentials_path):
                try:
                    print("Trying with service account...")
                    # Check if it's a web client or service account
                    with open(credentials_path, 'r') as f:
                        creds_data = json.load(f)
                    
                    if 'web' in creds_data:
                        print("Found web client credentials, not service account")
                    else:
                        # Assume it's a service account
                        credentials = service_account.IDTokenCredentials.from_service_account_file(
                            credentials_path,
                            target_audience=function_url
                        )
                        credentials.refresh(GoogleAuthRequest())
                        sa_id_token = credentials.token
                        
                        files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
                        headers = {'Authorization': f'Bearer {sa_id_token}'}
                        response = requests.post(function_url, files=files, headers=headers)
                        
                        if response.status_code == 200:
                            # Return the image as a response
                            django_response = HttpResponse(response.content, content_type='image/png')
                            django_response['Content-Disposition'] = 'attachment; filename="negative.png"'
                            return django_response
                        else:
                            print(f"Service account call failed with status {response.status_code}")
                except Exception as sa_error:
                    print(f"Service account error: {str(sa_error)}")
            else:
                print("No service account credentials found")
            
            # If we get here, all authentication methods failed
            return JsonResponse({
                'error': 'Failed to call the Cloud Function. Please check the logs for details.'
            }, status=500)
                
        except Exception as e:
            print(f"Proxy error: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'error': f'Proxy error: {str(e)}'}, status=500)
            
    def get(self, request):
        return JsonResponse({"message": "Negative image proxy is up. Use POST with an image file."})

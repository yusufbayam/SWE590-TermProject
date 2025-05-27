from locust import HttpUser, task, between
import random
import os
import json
from form_data_helper import create_form_data_for_image

class ProjectUserCustomFormData(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Initialize the user session"""
        os.makedirs("results", exist_ok=True)
        
        self.browser_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        
        self.client.headers.update({
            'Content-Type': 'application/json',
            **self.browser_headers
        })
    
    @task(3)
    def call_service1(self):
        """Test the Service1 hello endpoint"""
        with self.client.get(
            "/api/service1/hello/?input=LocustTest", 
            name="Service1 - Hello",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "message" in response_data:
                        response.success()
                    else:
                        response.failure("Response doesn't contain 'message' field")
                except json.JSONDecodeError:
                    response.failure("Response is not valid JSON")
            else:
                print(f"Service1 error: Status {response.status_code}, Content: {response.content[:200]}")
                response.failure(f"Got status code {response.status_code}")
    
    @task(2)
    def call_service2(self):
        """Test the Service2 evening endpoint"""
        with self.client.get(
            "/api/service2/evening/?input=LocustTest",
            name="Service2 - Evening",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "message" in response_data:
                        response.success()
                    else:
                        response.failure("Response doesn't contain 'message' field")
                except json.JSONDecodeError:
                    response.failure("Response is not valid JSON")
            else:
                print(f"Service2 error: Status {response.status_code}, Content: {response.content[:200]}")
                response.failure(f"Got status code {response.status_code}")
    
    @task(1)
    def process_image(self):
        """Test the negative image Cloud Function with different image sizes using custom form data"""
        image_sizes = ["small", "medium", "large"]
        selected_size = random.choice(image_sizes)
        
        image_path = f"test_images/{selected_size}.png"
        
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} does not exist, skipping image processing test")
            return
        
        try:
            body, content_type = create_form_data_for_image(image_path, field_name="file")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/png,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': self.host,
                'Referer': f"{self.host}/",
                'Content-Type': content_type
            }
            
            with self.client.request(
                "POST",
                "/api/service1/negative-image/",
                data=body,
                headers=headers,
                name=f"Cloud Function - Negative Image ({selected_size})",
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    # Check if response is an image
                    if response.headers.get('Content-Type', '').startswith('image/'):
                        response.success()
                    else:
                        print(f"Not an image response: {response.headers.get('Content-Type')}, Content: {response.content[:100]}")
                        response.failure("Response is not an image")
                else:
                    print(f"Cloud Function error: Status {response.status_code}")
                    print(f"Response headers: {dict(response.headers)}")
                    print(f"Response content: {response.content[:200]}")
                    response.failure(f"Got status code {response.status_code}")
                    
        except Exception as e:
            print(f"Exception in process_image: {str(e)}")
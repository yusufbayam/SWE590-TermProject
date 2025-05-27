from locust import HttpUser, task, between
import os
import time
import random
import csv
from datetime import datetime

class CloudFunctionUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup for the Cloud Function tests"""
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file_path = f"{self.results_dir}/cloud_function_performance_{timestamp}.csv"
        
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Timestamp', 'Image Size', 'Request Time (ms)', 'Response Size (bytes)', 'Success', 'Status Code', 'Error'])
    
    def log_metrics(self, image_size, request_time_ms, response_size, success, status_code=200, error=''):
        """Log detailed metrics to CSV file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, image_size, request_time_ms, response_size, success, status_code, error])
    
    @task
    def test_small_image(self):
        """Test with small image (~50KB)"""
        self._process_image("small")
    
    @task
    def test_medium_image(self):
        """Test with medium image (~500KB)"""
        self._process_image("medium")
    
    @task
    def test_large_image(self):
        """Test with large image (~2MB)"""
        self._process_image("large")
    
    def _process_image(self, size):
        """Process an image of the specified size"""
        image_path = f"test_images/{size}.png"
        
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} does not exist, skipping test")
            return
        
        file_size = os.path.getsize(image_path)
        
        start_time = time.time()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/png,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': self.host,
            'Referer': f"{self.host}/"
        }
        
        try:
            with open(image_path, "rb") as image_file:
                file_content = image_file.read()
            
            file_name = os.path.basename(image_path)
            
            files = {
                "file": (file_name, file_content, "image/png")
            }
            
            with self.client.post(
                "/api/service1/negative-image/",
                files=files,
                headers=headers,
                name=f"Cloud Function - {size.capitalize()} Image ({file_size/1024:.1f}KB)",
                catch_response=True
            ) as response:
                end_time = time.time()
                request_time_ms = (end_time - start_time) * 1000
                status_code = response.status_code
                success = status_code == 200
                error_msg = ''
                
                if success:
                    if response.headers.get('Content-Type', '').startswith('image/'):
                        response_size = len(response.content)
                        self.log_metrics(size, request_time_ms, response_size, True, status_code)
                        response.success()
                    else:
                        error_msg = f"Not an image: {response.headers.get('Content-Type')}"
                        print(f"ERROR: {error_msg}")
                        print(f"Content preview: {response.content[:100]}")
                        self.log_metrics(size, request_time_ms, len(response.content), False, status_code, error_msg)
                        response.failure(error_msg)
                else:
                    error_msg = f"HTTP {status_code}"
                    print(f"ERROR: Cloud Function returned {status_code}")
                    print(f"Headers: {dict(response.headers)}")
                    print(f"Content: {response.content[:200]}")
                    response_size = len(response.content) if response.content else 0
                    self.log_metrics(size, request_time_ms, response_size, False, status_code, error_msg)
                    response.failure(error_msg)
        except Exception as e:
            end_time = time.time()
            request_time_ms = (end_time - start_time) * 1000
            error_msg = str(e)
            print(f"EXCEPTION: {error_msg}")
            self.log_metrics(size, request_time_ms, 0, False, 0, error_msg)
            raise 
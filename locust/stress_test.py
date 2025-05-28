from locust import HttpUser, task, between, events
import time
import json
import os
import csv
from datetime import datetime

# Track global statistics
start_time = None
request_count = 0
success_count = 0
failure_count = 0
response_times = []

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global start_time, request_count, success_count, failure_count, response_times
    start_time = time.time()
    request_count = 0
    success_count = 0
    failure_count = 0
    response_times = []
    
    os.makedirs("results", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_file = f"results/stress_test_metrics_{timestamp}.csv"
    
    with open(metrics_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'Requests', 'Success Rate (%)', 'Avg Response Time (ms)', 'RPS', 'Failures'])
    

def record_stats():
    global start_time, request_count, success_count, failure_count, response_times
    
    if request_count == 0:
        return
    
    elapsed = time.time() - start_time
    success_rate = (success_count / request_count) * 100 if request_count > 0 else 0
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    rps = request_count / elapsed if elapsed > 0 else 0
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_file = f"results/stress_test_metrics_{timestamp}.csv"
    
    with open(metrics_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([round(elapsed, 1), request_count, round(success_rate, 2), 
                        round(avg_response_time, 2), round(rps, 2), failure_count])

class StressTestUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    def on_start(self):
        """Initialize browser-like headers"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
    
    @task(10)
    def rapid_service1_calls(self):
        """Make rapid calls to Service1"""
        global request_count, success_count, failure_count, response_times
        
        start = time.time()
        with self.client.get(
            "/api/service1/hello/?input=StressTest",
            name="Stress - Service1",
            headers=self.headers,
            catch_response=True
        ) as response:
            end = time.time()
            request_count += 1
            response_times.append((end - start) * 1000)  # ms
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "message" in data:
                        success_count += 1
                        response.success()
                    else:
                        failure_count += 1
                        print(f"Missing message field in response: {data}")
                        response.failure("Missing message field")
                except json.JSONDecodeError:
                    failure_count += 1
                    print(f"Invalid JSON response: {response.text[:200]}")
                    response.failure("Invalid JSON")
            else:
                failure_count += 1
                print(f"HTTP {response.status_code} from Service1: {response.text[:200]}")
                response.failure(f"HTTP {response.status_code}")
    
    @task(5)
    def rapid_service2_calls(self):
        """Make rapid calls to Service2"""
        global request_count, success_count, failure_count, response_times
        
        start = time.time()
        with self.client.get(
            "/api/service2/evening/?input=StressTest",
            name="Stress - Service2",
            headers=self.headers,
            catch_response=True
        ) as response:
            end = time.time()
            request_count += 1
            response_times.append((end - start) * 1000)  # ms
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "message" in data:
                        success_count += 1
                        response.success()
                    else:
                        failure_count += 1
                        print(f"Missing message field in response: {data}")
                        response.failure("Missing message field")
                except json.JSONDecodeError:
                    failure_count += 1
                    print(f"Invalid JSON response: {response.text[:200]}")
                    response.failure("Invalid JSON")
            else:
                failure_count += 1
                print(f"HTTP {response.status_code} from Service2: {response.text[:200]}")
                response.failure(f"HTTP {response.status_code}") 
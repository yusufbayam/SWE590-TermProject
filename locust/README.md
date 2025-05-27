# Performance Testing with Locust

This directory contains Locust test scripts for evaluating the performance of the SWE590 Term Project.

## Setup

1. Install Locust:
   ```
   pip install locust
   ```

2. Prepare test images:
   - Place test images in the `test_images` directory
   - Name them `small.png`, `medium.png`, and `large.png`

## Available Test Scripts

1. **locustfile.py** - General tests for all services
   - Tests service1 and service2 API endpoints
   - Tests the negative image Cloud Function
   - Simulates realistic user behavior

2. **cloud_function_test.py** - Detailed Cloud Function performance tests
   - Focuses on the image processing functionality
   - Measures performance with different image sizes
   - Collects detailed metrics in CSV format

3. **stress_test.py** - High load testing
   - Tests how the system handles rapid API requests
   - Focuses on throughput and error rates
   - Collects aggregate performance metrics

## Running the Tests

### Basic Test

```bash
locust -f locustfile.py --host=http://your-project-domain-or-ip
```

### Cloud Function Performance Test

```bash
locust -f cloud_function_test.py --host=http://your-project-domain-or-ip
```

### Stress Test

```bash
locust -f stress_test.py --host=http://your-project-domain-or-ip
```

## Test Parameters

Configure these parameters in the Locust web UI:

- **Number of users**: The peak number of concurrent users to simulate
- **Spawn rate**: How quickly to add users
- **Run time**: How long to run the test

## Recommended Test Scenarios

1. **Baseline Performance**:
   - 10 users, 1 user/second spawn rate
   - Run for 5 minutes
   - Use `locustfile.py`

2. **Cloud Function Scaling**:
   - 20 users, 2 users/second spawn rate
   - Run for 10 minutes
   - Use `cloud_function_test.py`

3. **API Stress Test**:
   - 100 users, 10 users/second spawn rate
   - Run for 5 minutes
   - Use `stress_test.py`

4. **Endurance Test**:
   - 50 users, 5 users/second spawn rate
   - Run for 30 minutes
   - Use `locustfile.py`

## Analyzing Results

Results are stored in the `results` directory:
- CSV files with detailed metrics
- Review the Locust web UI for real-time graphs
- Compare response times across different components
- Identify bottlenecks in the architecture

Use these results to optimize your GKE deployment, scaling configurations, and resource allocations. 
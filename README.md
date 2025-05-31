# Cloud-Native Architecture Project

This project implements a scalable, cloud-native architecture on Google Cloud Platform (GCP) integrating containerized workloads on Kubernetes, virtual machines, and serverless functions.

## Architecture Overview

The system consists of:
- **Frontend**: React-based web application deployed as a container
- **Backend Services**: Two Django microservices (service1 and service2)
- **Serverless Function**: Image processing function (negative filter)
- **Infrastructure**: Managed with Terraform for automated deployment

## Prerequisites

- [Google Cloud Platform Account](https://cloud.google.com/free) with $300 free credits
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) (v1.0.0 or higher)
- [Python](https://www.python.org/downloads/) (v3.9 or higher)
- [Node.js](https://nodejs.org/) (v16 or higher)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Google Cloud SDK

```bash
# Login to your Google Account
gcloud auth login

# Set the project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_ZONE=us-central1-a
```

### 4. Deploy Infrastructure with Terraform

```bash
cd terraform

# Initialize Terraform
terraform init

# Validate the configuration
terraform validate

# Review the plan
terraform plan -var="project_id=YOUR_PROJECT_ID"

# Apply the configuration
terraform apply -var="project_id=YOUR_PROJECT_ID"

# Note the outputs for later use
```

### 5. Connect to GKE Cluster

```bash
gcloud container clusters get-credentials YOUR_CLUSTER_NAME --zone YOUR_ZONE --project YOUR_PROJECT_ID
```

### 6. Setup Local Development Environment (Optional)

#### Set up Python virtual environments

```bash
# For service1
cd service1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# For service2
cd ../service2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# For cloud function
cd ../cloud_function
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# For Locust performance testing
cd ../locust
python -m venv locust_venv
source locust_venv/bin/activate
pip install -r requirements.txt
deactivate
```

#### Setup Frontend

```bash
cd ../frontend
npm install
```

### 7. Run Locally with Docker Compose (Optional)

```bash
# From the root directory
docker-compose up --build
```

This will start:
- Frontend at http://localhost:3001
- Service1 at http://localhost:8001
- Service2 at http://localhost:8002

### 8. Performance Testing with Locust

```bash
cd locust
source locust_venv/bin/activate

# Generate test images if needed
python generate_test_images.py

# Run the Locust tests
python -m locust -f locustfile.py --host=YOUR_DEPLOYED_FRONTEND_URL
```

Then open http://localhost:8089 in your browser to access the Locust web interface.

## Project Structure

- `frontend/`: React web application
- `service1/`: Django microservice 1
- `service2/`: Django microservice 2  
- `cloud_function/`: Serverless function for image processing
- `terraform/`: IaC configuration for GCP resources
- `locust/`: Performance testing scripts and configuration

## Cleaning Up Resources

To avoid incurring charges, remember to destroy all created resources when done:

```bash
cd terraform
terraform destroy -var="project_id=YOUR_PROJECT_ID"
```

## Troubleshooting

- **Terraform Errors**: Check the GCP permissions and API enablement
- **Kubernetes Connectivity**: Verify network settings and firewall rules
- **Cloud Function Deployment**: Check logs in GCP Console

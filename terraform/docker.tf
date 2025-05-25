# Configure Docker image building and publishing to Artifact Registry

# Reference existing Artifact Registry repository instead of creating a new one
data "google_artifact_registry_repository" "docker_repo" {
  provider      = google
  location      = "us-central1"
  repository_id = "swe590-project-images"
  project       = var.project_id
}

# Build and push frontend image
resource "null_resource" "build_frontend_image" {
  triggers = {
    # Rebuild when any of these files change
    frontend_dockerfile_hash = filesha256("${path.module}/../frontend/Dockerfile")
    frontend_app_hash = filesha256("${path.module}/../frontend/src/App.js")
    frontend_nginx_hash = filesha256("${path.module}/../frontend/nginx.conf")
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Set up authentication for Docker to Artifact Registry
      gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      
      # Build the frontend image
      docker build -t us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/frontend:latest ${path.module}/../frontend
      
      # Push the image to Artifact Registry
      docker push us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/frontend:latest
    EOT
  }
}

# Build and push service1 image
resource "null_resource" "build_service1_image" {
  triggers = {
    # Rebuild when any of these files change
    service1_dockerfile_hash = filesha256("${path.module}/../service1/Dockerfile")
    service1_views_hash = filesha256("${path.module}/../service1/hello_app/views.py")
    service1_urls_hash = filesha256("${path.module}/../service1/hello_app/urls.py")
    service1_requirements_hash = filesha256("${path.module}/../service1/requirements.txt")
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Set up authentication for Docker to Artifact Registry
      gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      
      # Build the service1 image
      docker build -t us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service1:latest ${path.module}/../service1
      
      # Push the image to Artifact Registry
      docker push us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service1:latest
    EOT
  }
}

# Build and push service2 image
resource "null_resource" "build_service2_image" {
  triggers = {
    # Rebuild when any of these files change
    service2_dockerfile_hash = filesha256("${path.module}/../service2/Dockerfile")
    service2_views_hash = filesha256("${path.module}/../service2/evening_app/views.py")
    service2_urls_hash = filesha256("${path.module}/../service2/evening_app/urls.py")
    service2_requirements_hash = filesha256("${path.module}/../service2/requirements.txt")
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Set up authentication for Docker to Artifact Registry
      gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
      
      # Build the service2 image
      docker build -t us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service2:latest ${path.module}/../service2
      
      # Push the image to Artifact Registry
      docker push us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service2:latest
    EOT
  }
}

# Output the image URLs for reference
output "frontend_image_url" {
  value = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/frontend:latest"
}

output "service1_image_url" {
  value = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service1:latest"
}

output "service2_image_url" {
  value = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service2:latest"
} 
#!/bin/bash
set -e

# Configuration
PROJECT_ID="white-site-459410-c0"
REGISTRY="us-central1-docker.pkg.dev/${PROJECT_ID}/swe590-project-images"
VERSION=$(date +"%Y%m%d%H%M%S")  # Use timestamp as version

echo "Building and pushing images with version: ${VERSION}"

# Build and push frontend image
echo "Building frontend image..."
cd ../frontend
docker build --platform linux/amd64 -t ${REGISTRY}/frontend:${VERSION} -t ${REGISTRY}/frontend:latest .
docker push ${REGISTRY}/frontend:${VERSION}
docker push ${REGISTRY}/frontend:latest
cd ../terraform

# Build and push service1 image
echo "Building service1 image..."
cd ../service1
docker build --platform linux/amd64 -t ${REGISTRY}/service1:${VERSION} -t ${REGISTRY}/service1:latest .
docker push ${REGISTRY}/service1:${VERSION}
docker push ${REGISTRY}/service1:latest
cd ../terraform

# Build and push service2 image
echo "Building service2 image..."
cd ../service2
docker build --platform linux/amd64 -t ${REGISTRY}/service2:${VERSION} -t ${REGISTRY}/service2:latest .
docker push ${REGISTRY}/service2:${VERSION}
docker push ${REGISTRY}/service2:latest
cd ../terraform

# Update the versions.tf file with new image versions
cat > versions.tf << EOF
# This file is auto-generated - DO NOT EDIT MANUALLY
variable "image_versions" {
  type = object({
    frontend = string
    service1 = string
    service2 = string
  })
  default = {
    frontend = "${VERSION}"
    service1 = "${VERSION}"
    service2 = "${VERSION}"
  }
}
EOF

echo "Updated versions.tf with new image versions"
echo "Run 'terraform apply -var=\"project_id=${PROJECT_ID}\"' to deploy the new versions" 
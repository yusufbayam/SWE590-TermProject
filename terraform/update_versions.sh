#!/bin/bash
set -e

# Check if all required arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <project_id> <frontend_version> <service1_version> <service2_version>"
    echo "Example: $0 white-site-459410-c0 20240601123456 20240601123456 20240601123456"
    exit 1
fi

PROJECT_ID="$1"
FRONTEND_VERSION="$2"
SERVICE1_VERSION="$3"
SERVICE2_VERSION="$4"

# Update the versions.tf file with specified image versions
cat > versions.tf << EOF
# This file is auto-generated - DO NOT EDIT MANUALLY
variable "image_versions" {
  type = object({
    frontend = string
    service1 = string
    service2 = string
  })
  default = {
    frontend = "${FRONTEND_VERSION}"
    service1 = "${SERVICE1_VERSION}"
    service2 = "${SERVICE2_VERSION}"
  }
}
EOF

echo "Updated versions.tf with specified image versions:"
echo "  frontend: ${FRONTEND_VERSION}"
echo "  service1: ${SERVICE1_VERSION}"
echo "  service2: ${SERVICE2_VERSION}"
echo ""
echo "Run 'terraform apply -var=\"project_id=${PROJECT_ID}\"' to apply these changes" 
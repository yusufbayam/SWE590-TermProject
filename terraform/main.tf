resource "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"
  
  # Enable Horizontal Pod Autoscaling
  addons_config {
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name

  node_count = var.gke_num_nodes
  
  # Enable node pool autoscaling
  autoscaling {
    min_node_count = var.node_pool_autoscaling.min_node_count
    max_node_count = var.node_pool_autoscaling.max_node_count
  }

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 30
    disk_type    = "pd-standard"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}

data "google_client_config" "default" {}

provider "kubernetes" {
    host                   = google_container_cluster.primary.endpoint
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
}

# --- Frontend Deployment ---
resource "kubernetes_deployment" "frontend" {
  metadata {
    name = "frontend"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "frontend"
      }
    }
    template {
      metadata {
        labels = {
          app = "frontend"
        }
      }
      spec {
        container {
          name  = "frontend"
          image = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/frontend:${var.image_versions.frontend}"
          port {
            container_port = 80
          }
          resources {
            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

# --- Service1 Deployment ---
resource "kubernetes_deployment" "service1" {
  metadata {
    name = "service1"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "service1"
      }
    }
    template {
      metadata {
        labels = {
          app = "service1"
        }
      }
      spec {
        container {
          name  = "service1"
          image = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service1:${var.image_versions.service1}"
          port {
            container_port = 8000
          }
          resources {
            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

# --- Service2 Deployment ---
resource "kubernetes_deployment" "service2" {
  metadata {
    name = "service2"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "service2"
      }
    }
    template {
      metadata {
        labels = {
          app = "service2"
        }
      }
      spec {
        container {
          name  = "service2"
          image = "us-central1-docker.pkg.dev/${var.project_id}/swe590-project-images/service2:${var.image_versions.service2}"
          port {
            container_port = 8000
          }
          resources {
            limits = {
              cpu    = "200m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
          }
        }
      }
    }
  }
}

# --- Frontend Service ---
resource "kubernetes_service" "frontend" {
  metadata {
    name = "frontend"
  }
  spec {
    selector = {
      app = "frontend"
    }
    port {
      port        = 80
      target_port = 80
    }
    type = "NodePort"
  }
}

# --- Service1 Service ---
resource "kubernetes_service" "service1" {
  metadata {
    name = "service1"
  }
  spec {
    selector = {
      app = "service1"
    }
    port {
      port        = 8000
      target_port = 8000
    }
    type = "NodePort"
  }
}

# --- Service2 Service ---
resource "kubernetes_service" "service2" {
  metadata {
    name = "service2"
  }
  spec {
    selector = {
      app = "service2"
    }
    port {
      port        = 8000
      target_port = 8000
    }
    type = "NodePort"
  }
}

# --- Ingress ---
resource "kubernetes_ingress_v1" "main" {
  metadata {
    name = "swe590-project-ingress"
    annotations = {
      "kubernetes.io/ingress.class"      = "gce"
      "kubernetes.io/ingress.allow-http" = "true"
    }
  }
  spec {
    rule {
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.frontend.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
        path {
          path      = "/service1"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.service1.metadata[0].name
              port {
                number = 8000
              }
            }
          }
        }
        path {
          path      = "/service2"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.service2.metadata[0].name
              port {
                number = 8000
              }
            }
          }
        }
      }
    }
  }
}

# --- Frontend Horizontal Pod Autoscaler ---
resource "kubernetes_horizontal_pod_autoscaler_v2" "frontend_hpa" {
  metadata {
    name = "frontend-hpa"
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.frontend.metadata[0].name
    }

    min_replicas = var.frontend_autoscaling.min_replicas
    max_replicas = var.frontend_autoscaling.max_replicas

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = var.frontend_autoscaling.cpu_utilization_target
        }
      }
    }

    behavior {
      scale_up {
        stabilization_window_seconds = 60
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 30
        }
      }
      scale_down {
        stabilization_window_seconds = 300
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 60
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.frontend
  ]
}

# --- Service1 Horizontal Pod Autoscaler ---
resource "kubernetes_horizontal_pod_autoscaler_v2" "service1_hpa" {
  metadata {
    name = "service1-hpa"
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.service1.metadata[0].name
    }

    min_replicas = var.service1_autoscaling.min_replicas
    max_replicas = var.service1_autoscaling.max_replicas

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = var.service1_autoscaling.cpu_utilization_target
        }
      }
    }

    behavior {
      scale_up {
        stabilization_window_seconds = 60
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 30
        }
      }
      scale_down {
        stabilization_window_seconds = 300
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 60
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.service1
  ]
}

# --- Service2 Horizontal Pod Autoscaler ---
resource "kubernetes_horizontal_pod_autoscaler_v2" "service2_hpa" {
  metadata {
    name = "service2-hpa"
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.service2.metadata[0].name
    }

    min_replicas = var.service2_autoscaling.min_replicas
    max_replicas = var.service2_autoscaling.max_replicas

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = var.service2_autoscaling.cpu_utilization_target
        }
      }
    }

    behavior {
      scale_up {
        stabilization_window_seconds = 60
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 30
        }
      }
      scale_down {
        stabilization_window_seconds = 300
        select_policy                = "Max"
        policy {
          type           = "Percent"
          value          = 100
          period_seconds = 60
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.service2
  ]
}

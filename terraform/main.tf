resource "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name

  node_count = var.gke_num_nodes

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
          image = "us-central1-docker.pkg.dev/white-site-459410-c0/swe590-project-images/frontend:latest"
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
          image = "us-central1-docker.pkg.dev/white-site-459410-c0/swe590-project-images/service1:latest"
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
    replicas = 1
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
          image = "us-central1-docker.pkg.dev/white-site-459410-c0/swe590-project-images/service2:latest"
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
    type = "ClusterIP"
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
    type = "ClusterIP"
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
    type = "ClusterIP"
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
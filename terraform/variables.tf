variable "project_id" {
  description = "white-site-459410-c0"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1-a"
}

variable "gke_cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "swe590-cluster"
}

variable "gke_num_nodes" {
  description = "Number of nodes in the default node pool"
  type        = number
  default     = 2
}

variable "frontend_autoscaling" {
  description = "Autoscaling configuration for frontend"
  type = object({
    min_replicas = number
    max_replicas = number
    cpu_utilization_target = number
  })
  default = {
    min_replicas = 1
    max_replicas = 3
    cpu_utilization_target = 70
  }
}

variable "service1_autoscaling" {
  description = "Autoscaling configuration for service1"
  type = object({
    min_replicas = number
    max_replicas = number
    cpu_utilization_target = number
  })
  default = {
    min_replicas = 2
    max_replicas = 5
    cpu_utilization_target = 70
  }
}

variable "service2_autoscaling" {
  description = "Autoscaling configuration for service2"
  type = object({
    min_replicas = number
    max_replicas = number
    cpu_utilization_target = number
  })
  default = {
    min_replicas = 2
    max_replicas = 5
    cpu_utilization_target = 70
  }
}

variable "node_pool_autoscaling" {
  description = "Autoscaling configuration for the node pool"
  type = object({
    min_node_count = number
    max_node_count = number
  })
  default = {
    min_node_count = 1
    max_node_count = 3
  }
}
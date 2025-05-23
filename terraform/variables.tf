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
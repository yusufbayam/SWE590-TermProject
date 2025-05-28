resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-bucket"
  location = "us-central1"
  force_destroy = true
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "function-source.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = "${path.module}/../cloud_function/function-source.zip"
}

resource "google_cloudfunctions_function" "negative_image" {
  name        = "negative-image-function"
  description = "Returns the negative of an uploaded image"
  runtime     = "python310"
  entry_point = "negative_image"
  region      = "us-central1"

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  trigger_http = true
  available_memory_mb = 512
  timeout = 60

  max_instances = 10
  min_instances = 1
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.negative_image.project
  region         = google_cloudfunctions_function.negative_image.region
  cloud_function = google_cloudfunctions_function.negative_image.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
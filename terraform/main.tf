resource "google_cloudfunctions2_function" "myfunction" {
  name     = "myfunction"
  location = "us-central1"

  build_config {
    runtime     = "nodejs16"
    entry_point = "helloHttp"
  }

  service_config {
    max_instance_count = 1
    available_memory   = "256M"
    timeout            = "60s"
  }
}
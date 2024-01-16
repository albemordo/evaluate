provider "google" {
  project = "my_project"
  region = "us-central1"
}

resource "google_storage_bucket" "my_storage_bucket" {
  name = "my_storage_bucket"
  location = "US"
}
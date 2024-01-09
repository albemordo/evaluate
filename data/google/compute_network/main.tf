resource "google_compute_network" "vpc" {
  project                 = "my-project-name"
  name                    = "vpc"
  auto_create_subnetworks = true
  mtu                     = 1460
}
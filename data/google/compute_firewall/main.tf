resource "google_compute_firewall" "my_rules" {
  project     = "my-project-name"
  name        = "my_rules"
  network     = "default"

  allow {
    protocol  = "tcp"
    ports     = ["80", "8080", "1000-2000"]
  }

}
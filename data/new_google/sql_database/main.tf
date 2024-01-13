resource "google_sql_database_instance" "instance" {
  name             = "instance"
  database_version = "POSTGRES_15"
  region           = "us-central1"

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name     = "database"
  instance = google_sql_database_instance.instance.name
}
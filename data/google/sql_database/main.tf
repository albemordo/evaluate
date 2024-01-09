resource "google_sql_database" "database" {
  name     = "my-database"
  instance = google_sql_database_instance.instance.name
}


resource "google_sql_database_instance" "instance" {
  name             = "instance"
  region           = "us-central1"
  database_version = "MYSQL_8_0"

  deletion_protection  = "true"
}
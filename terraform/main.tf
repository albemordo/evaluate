resource "google_storage_bucket" "website-static-bucket" {
  name          = "my_bucket"
  location      = "EU"
  force_destroy = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  cors {
    origin_policy = 4
    cors_rule {
      max_age_seconds = 86400
      allow_credentials = true
      allow_headers = ["Allowed header"]
      allow_methods = ["Allowed method"]
      expose_headers = ["Exposed header"]
      max_age_seconds = 86400
      is_public_policy = 4
      origin_policy = 4
      preflight_method = "Allowed preflight method"
      response_header = "Response header"
      response_policy = 4
      allow_credentials = true
      allow_headers = ["Allowed header"]
      allow_methods = ["Allowed method"]
      expose_headers = ["Exposed header"]
      max_age_seconds = 86400
      is_public_policy = 4
      origin_policy = 4
      preflight_method = "Allowed preflight method"
      response_header = "Response header"
      response_policy = 4
    }
  }
}
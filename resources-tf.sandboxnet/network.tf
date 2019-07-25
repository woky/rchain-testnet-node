resource "google_compute_network" "vpc_network" {
  name = "${var.resources_name}-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "vpc_subnet" {
  name = "${var.resources_name}-subnet"
  ip_cidr_range = "10.6.0.0/24"
  region = var.gcp_region
  network = google_compute_network.vpc_network.self_link
}

resource "google_compute_firewall" "fw_public_node" {
  name = "${var.resources_name}-fw-public"
  network = google_compute_network.vpc_network.self_link
  priority = 500
  allow {
    protocol = "tcp"
    ports = [ 22 ]
  }
}

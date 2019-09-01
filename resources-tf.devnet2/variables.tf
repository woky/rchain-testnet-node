variable "network_id"   { default = "devnet2" }
variable "domain"       { default = "devnet2.rchain-dev.tk" }
variable "node_count"   { default = 8 }
variable "gcp_zone"     { default = "us-east1-d" }
variable "machine_type" { default = "n1-highmem-2" }
variable "os_image"     { default = "ubuntu-os-cloud/ubuntu-1804-lts" }
variable "disk_size"    { default = 200 }
variable "disk_type"    { default = "pd-standard" }

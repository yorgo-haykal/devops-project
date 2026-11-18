terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

variable "env_name" { type = string }
variable "image" { type = string }
variable "external_port" { type = number }

module "webapp" {
  source        = "../../modules/webapp"
  env_name      = var.env_name
  image         = var.image
  external_port = var.external_port
}

output "app_url" {
  value = module.webapp.app_url
}

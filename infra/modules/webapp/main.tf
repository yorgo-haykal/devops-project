terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

resource "docker_image" "app" {
  name = var.image
}

resource "docker_container" "web" {
  name  = "${var.env_name}-web"
  image = docker_image.app.image_id

  ports {
    internal = 80
    external = var.external_port
  }
}

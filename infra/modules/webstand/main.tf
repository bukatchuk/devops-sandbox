terraform {
  required_providers {
    docker = { source = "kreuzwerker/docker" }
  }
}

resource "docker_image" "web" {
  name         = var.image
  keep_locally = true
}

resource "docker_network" "net" {
  name = "${var.name_prefix}-net"
}

resource "docker_container" "web" {
  count   = var.replicas
  name    = "${var.name_prefix}-web-${count.index}"
  image   = docker_image.web.image_id
  restart = "unless-stopped"
  networks_advanced {
    name = docker_network.net.name
  }
}

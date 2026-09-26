terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

variable "image" {
  description = "Образ приложения (тег закрепляется — политика запрещает latest)"
  type        = string
  default     = "nginx:1.29-alpine"
}

module "web" {
  source      = "./modules/webstand"
  name_prefix = "l1108"
  image       = var.image
  replicas    = 2
}

output "web_containers" {
  description = "Контейнеры учебного стенда"
  value       = module.web.container_names
}

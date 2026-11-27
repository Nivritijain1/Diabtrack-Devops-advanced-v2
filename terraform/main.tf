terraform {
  required_providers {
    docker = {
      source  = "registry.opentofu.org/kreuzwerker/docker"
      version = "4.7.0"
    }
  }
}

provider "docker" {}
resource "docker_image" "diabtrack" {
  name = "diabtrack:latest"

  build {
    context = "../app"
  }
}

resource "docker_network" "diabtrack_network" {
  name = "diabtrack-network"
}

resource "docker_container" "testing" {
  name  = "diabtrack-testing"
  image = docker_image.diabtrack.image_id

  ports {
    internal = 8501
    external = 8502
  }

  networks_advanced {
    name = docker_network.diabtrack_network.name
  }
}

resource "docker_container" "production" {
  name  = "diabtrack-production"
  image = docker_image.diabtrack.image_id

  ports {
    internal = 8501
    external = 8503
  }

  networks_advanced {
    name = docker_network.diabtrack_network.name
  }
}

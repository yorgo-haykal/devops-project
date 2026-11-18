terraform {
  backend "local" {}

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

variable "pr_number" { type = string }
variable "image" { type = string }

variable "owner" {
  type    = string
  default = "leanna"
}

variable "expires" {
  type    = string
  default = "2026-11-25"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "preview" {
  metadata {
    name = "pr-${var.pr_number}"
    labels = {
      purpose = "preview"
      pr      = var.pr_number
      owner   = var.owner
      expires = var.expires
    }
  }
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "myapp"
    namespace = kubernetes_namespace.preview.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = { app = "myapp" }
    }

    template {
      metadata {
        labels = { app = "myapp" }
      }

      spec {
        container {
          name  = "myapp"
          image = var.image

          # The Session 2 Flask app listens on 5000 (not 3000)
          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app" {
  metadata {
    name      = "myapp"
    namespace = kubernetes_namespace.preview.metadata[0].name
  }

  spec {
    selector = { app = "myapp" }

    port {
      port        = 80
      target_port = 5000
    }

    type = "ClusterIP"
  }
}


terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }

  backend "local" {}
}

variable "pr_number" {
  type        = string
  description = "Pull Request number used to create the preview environment"
}

variable "image" {
  type        = string
  description = "Container image pinned to a SHA256 digest"

  validation {
    condition     = can(regex("@sha256:[a-f0-9]{64}$", var.image))
    error_message = "The image must be pinned to a SHA256 digest."
  }
}

provider "kubernetes" {
  config_path = pathexpand("~/.kube/config")
}

resource "kubernetes_namespace" "preview" {
  metadata {
    name = "pr-${var.pr_number}"

    labels = {
      purpose = "preview"
      pr      = var.pr_number
      owner   = "devops-team"
    }
  }
}

resource "kubernetes_deployment" "app" {
  #checkov:skip=CKV_K8S_14:Image digest is enforced by Terraform variable validation
  #checkov:skip=CKV_K8S_43:Image digest is enforced by Terraform variable validation

  metadata {
    name      = "myapp"
    namespace = kubernetes_namespace.preview.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "myapp"
      }
    }

    template {
      metadata {
        labels = {
          app = "myapp"
        }
      }

      spec {
        security_context {
          run_as_non_root = true
          run_as_user     = 1000
          run_as_group    = 1000
        }

        container {
          name              = "myapp"
          image             = var.image
          image_pull_policy = "Always"

          security_context {
            run_as_non_root            = true
            run_as_user                = 1000
            allow_privilege_escalation = false
            read_only_root_filesystem  = true

            capabilities {
              drop = ["ALL"]
            }
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "64Mi"
            }

            limits = {
              cpu    = "250m"
              memory = "128Mi"
            }
          }

          port {
            container_port = 5000
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = 5000
            }

            initial_delay_seconds = 5
            period_seconds        = 10
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 5000
            }

            initial_delay_seconds = 15
            period_seconds        = 20
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
    selector = {
      app = "myapp"
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "ClusterIP"
  }
}

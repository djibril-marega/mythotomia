terraform {
  cloud {
    organization = "mythotomia"

    workspaces {
      project = "Web Site"
      name = "production"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.92"
    }
  }

  required_version = ">= 1.2.0"
}

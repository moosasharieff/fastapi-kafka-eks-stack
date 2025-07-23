
module "vpc" {
  source = "./modules/vpc"

  project = var.project

}

module "eks" {
  source = "./modules/eks"

  project      = var.project
  cluster_name = var.cluster_name

}

module "vpc" {
  source = "./modules/vpc"

  project = var.project

}

module "eks" {
  source = "./modules/eks"

  project            = var.project
  cluster_name       = var.cluster_name
  private_subnet_ids = module.vpc.private_subnet_ids
  eks_instance_type  = var.eks_instance_type

}

module "security_groups" {
  source = "./modules/security_groups"

  vpc_id = module.vpc.vpc_id
}
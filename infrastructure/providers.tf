

provider "aws" {
  region  = "eu-west-1"
  profile = "default"
}


provider "kubernetes" {
  host = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority)
  token = data.aws_eks_cluster_auth.main.token
}

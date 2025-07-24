

variable "project" {
  type = string
  description = "Name of this project."
}

variable "cluster_name" {
  type = string
  description = "Cluster name of EKS Service"
}

variable "private_subnet_ids" {
  type = list(string)
  description = "Private subnets ids created in vpc module"
}

variable "eks_instance_type" {
  type = list(string)
  description = "EC2 Instance Types in EKS Nodes"
}
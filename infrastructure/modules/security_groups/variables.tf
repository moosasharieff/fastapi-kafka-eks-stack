

variable "rds_ingress_cidr_blocks" {
  description = "CIDR Blocks that are allowed to access RDS instance (e.g. EKS Nodes)"
  type = list(string)
  default = ["0.0.0.0/0"]
}

variable "vpc_id" {
  description = "ID of VPC of which this security group is to be part off"
  type = string
}


variable "db_name" {
  type = string
  description = "Name of RDS PostgreSQL Database"
}

variable "private_subnet_ids" {
  type = list(string)
  description = "List of Private subnet ids within a VPC"
}

variable "db_username" {
  type = string
  description = "Username of RDS PostgreSQL Database"
}

variable "db_password" {
  type = string
  description = "Password of RDS PostgreSQL Database"
  sensitive = true
}

variable "security_group_ids" {
  type = list(string)
  description = "Security Group of VPC"
}

variable "db_instance_count" {
  type = number
  description = "Number of RDS PostgreSQL Database Instances"
}

variable "db_instance_class" {
  type = string
  description = "Class type of DB instance"
}
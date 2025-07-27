

resource "aws_db_subnet_group" "main" {
  name        = "${var.db_name}-subnet-group"
  subnet_ids  = var.private_subnet_ids
  description = "RDS subnet group for PostgreSQL."

  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}


resource "aws_rds_cluster" "main" {
  cluster_identifier      = var.db_name
  engine                  = "aurora-postgresql"
  master_username         = var.db_username
  master_password         = var.db_password
  database_name           = var.db_name
  backup_retention_period = 7
  storage_encrypted       = true
  engine_version          = "13.4"
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = var.security_group_ids

  tags = {
    Name = "${var.db_name}-cluster"
  }

  depends_on = [
    aws_db_subnet_group.main
  ]

}

resource "aws_rds_cluster_instance" "main" {
  count                = var.db_instance_count
  cluster_identifier   = aws_rds_cluster.main.id
  instance_class       = var.db_instance_class
  engine               = "aurora-postgresql"
  publicly_accessible  = false
  db_subnet_group_name = aws_db_subnet_group.main.name

  tags = {
    Name = "${var.db_name}-instance-${count.index}"
  }

}
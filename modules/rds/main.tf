resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Environment = var.environment
  }
}

resource "aws_security_group" "rds" {
  name   = "${var.environment}-rds-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
    description = "Allow PostgreSQL from VPC"
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
    description = "Allow outbound PostgreSQL within VPC"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier              = "${var.environment}-db"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = var.instance_class

  allocated_storage       = 20
  storage_type            = "gp3"

  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password

  multi_az                = var.environment == "prod" ? true : false

  
  skip_final_snapshot       = false
  final_snapshot_identifier = "${var.environment}-db-final-snapshot"

  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]

  backup_retention_period = var.environment == "prod" ? 7 : 1

  tags = {
    Environment = var.environment
  }
}

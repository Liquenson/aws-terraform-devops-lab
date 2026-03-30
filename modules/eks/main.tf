resource "aws_eks_cluster" "main" {
  name     = "${var.environment}-cluster"
  role_arn = var.eks_cluster_role_arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.private_subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true 
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator"]
  tags = { Environment = var.environment }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.environment}-nodes"
  node_role_arn   = var.eks_nodes_role_arn
  subnet_ids      = var.private_subnet_ids
  instance_types  = [var.instance_type]

  scaling_config {
    desired_size = var.desired_capacity
    min_size     = var.min_capacity
    max_size     = var.max_capacity
  }

  update_config { max_unavailable = 1 }
  depends_on = [aws_eks_cluster.main]
}

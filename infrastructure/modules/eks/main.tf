

resource "aws_eks_cluster" "main" {
  name = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  version = "1.31"

  vpc_config {
    subnet_ids = var.private_subnet_ids
  }

  depends_on = [aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy]

}


resource "aws_eks_node_group" "default" {
  cluster_name = aws_eks_cluster.main.name
  node_group_name = "${var.project}-${var.cluster_name}-node-group"
  node_role_arn = aws_iam_role.eks_node_role.arn
  subnet_ids = var.private_subnet_ids

  scaling_config {
    desired_size = 2
    max_size = 4
    min_size = 1
  }

  instance_types = var.eks_instance_type
  disk_size = 20
  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly
  ]

}


resource "kubernetes_config_map" "aws_auth" {
  metadata {
    name = "aws-auth"
    namespace = "kube-system"
  }

  data = {
    mapRoles = yamlencode([
      {
        rolearn = aws_iam_role.eks_node_role.arn
        username = "system:node:{{EC2PrivateDNSName}}"
        group = [
          "system:bootstrappers",
          "system:nodes"
        ]
      }])
  }

  depends_on = [aws_eks_node_group.default]
}

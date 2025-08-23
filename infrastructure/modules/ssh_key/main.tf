# Generate a new SSH Key
resource "tls_private_key" "eks_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

# Register it in AWS
resource "aws_key_pair" "eks_key" {
  key_name = var.key_name
  public_key = tls_private_key.eks_key.public_key_openssh
}

# Save private key locally
resource "local_file" "private_key" {
  content = tls_private_key.eks_key.private_key_openssh
  filename = var.private_key_path
}

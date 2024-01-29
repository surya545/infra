module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "eks-vpc"
  cidr = var.vpc_cidr

  azs = data.aws_availability_zones.azs.names

  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_dns_hostnames = true
  enable_nat_gateway   = true
  single_nat_gateway   = true

  tags = {
    "kubernetes.io/cluster/my-eks-cluster" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/my-eks-cluster" = "shared"
    "kubernetes.io/role/elb"               = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/my-eks-cluster" = "shared"
    "kubernetes.io/role/internal-elb"      = 1
  }

}


resource "aws_iam_policy" "eks_policy_extension" {
  name        = "eks_policy"
  path        = "/"
  description = "My eks policy"
  policy = file("iam-policy.json")
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "my-eks-cluster"
  cluster_version = "1.24"

  cluster_endpoint_public_access = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    nodes = {
      min_size     = 1
      max_size     = 3
      desired_size = 2

      instance_type = ["t2.small"]
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

output "nodegroup_iam_role" {
  value = module.eks.eks_managed_node_groups.nodes.iam_role_name
}

resource "aws_iam_role_policy_attachment" "eks_worker_nodes_policy_attachment" {
  policy_arn = aws_iam_policy.eks_policy_extension.arn
  role       = module.eks.eks_managed_node_groups.nodes.iam_role_name
}


resource "aws_iam_policy" "alb_ingress_controller_policy" {
  name        = "ALBIngressControllerIAMPolicy"
  description = "IAM policy for ALB Ingress Controller"
  policy      = file("${path.module}/iam-policy.json") # Provide the path to your IAM policy document
}

resource "null_resource" "generate_iam_policy" {
  provisioner "local-exec" {
    command = <<EOF
      cat <<EOF2 > eks-ingress-trust-iam-policy.json
{
    "Version":"2012-10-17",
    "Statement":[
        {
          "Effect":"Allow",
          "Principal":{
              "Federated":"${module.eks.oidc_provider_arn}"
          },
          "Action":"sts:AssumeRoleWithWebIdentity",
          "Condition":{
              "StringEquals":{
              "${module.eks.oidc_provider}:aud": "sts.amazonaws.com",
              "${module.eks.oidc_provider}:sub":"system:serviceaccount:kube-system:alb-ingress-controller"
              }
          }
        }
    ]
  }
  EOF2
EOF
  }

  depends_on = [module.eks]
}

#  Creating EKS Cluster with Ingress Controller

This repository contains a Terraform application that can bring up an working EKS Cluster at once.

## Prerequisites

Before getting started, ensure you have the following installed:

- Terraform: [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
- kubectl: [Install Kubectl](https://kubernetes.io/docs/tasks/tools/)
- awscli: [Install Kubectl](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Configue aws cli


## Getting Started

Follow these steps to bring up a EKS Cluster with ALB Ingress Controller setup:

1. **Move to the Directory**:

   ```bash
   cd eks-cluster

2. **Deploy the essential aws resources using terraform**:

   ```bash
   terraform init
   terraform plan
   terraform apply

4. **Setup ALB Ingress Controller**:

    Follow the steps,
   [Ingress Controller] (https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
   you will end up replacing all my files with your own configs.

5. **Set kubectl context to eks**:

   [Link] (https://jamesdefabia.github.io/docs/user-guide/kubectl/kubectl_config_set-context/)

6. **Apply the resources needed by ALB using kubectl***:

   ```bash
   kubectl apply -f .


# Things we Achieved

1. Used terraform to set up a kubernetes cluster.
2. Loaded Ingress Controller.
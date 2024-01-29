# Deploy Jenkins and Use it for CI CD
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
   cd jenkins

2. **Deploy the essential aws resources using terraform**:

   ```bash
   terraform init
   terraform plan
   terraform apply


# Things we Achieved

1. Deployed Jenkins on EC2 to manage CI/CD for both app and infra
# Dockerizing Flask Application

This repository contains a Flask application that is dockerized for easy deployment and scalability.

## Prerequisites

Before getting started, ensure you have the following installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)


## Getting Started

Follow these steps to run the Flask application locally using Docker:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Build the Docker Image**:

   ```bash
   docker build -t message-service:v1.0 .

3. **Create Image Repository in ECR and Login***:

Follow link https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html
For simplicity we will use Public Repo

4. **Push to ECR**:

   ```bash
   docker tag message-service:v1.0 public.ecr.aws/XXXXX/message-service:v1.0  \# replace the url given by your console
   docker push public.ecr.aws/XXXXX/message-service:v1.0  \# replace the url given by your console

5. **Create EKS Cluster with ALB Ingress Controller and Install AWS EBS CSI Driver**:

   check under eks-cluster folder in this repo

   ```bash
    kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.27"


6. **Zero downtime deployments (along with sidecars fluentd), service spec, ingress spec**:

    check config files to see the implementation
    app-service.yml
    app-deployment.yml
    app-ingress.yml

7. **Create MySQL deployment to use as DB, using statefulset along with a storage**:

    check config files to see the implementation
    mysql-secrets
    mysql-service.yml
    mysql-stateful.yml
    mysql-storage-class.yml

8. **Connect Flask App to MySQL**:

    \# Replace these fields from  mysql-secrets.yml  Use base64 encoded values

    root-password: <base64 rootpass>
    database-name: <base64 db>
    user: <base64 user>
    password: <base64 pass>

    generate  
        ```bash
        echo -n 'input' | openssl base64
  
9. **Deploy the application**:

    ```bash
        kubectl apply -f .



# Things we Achieved

1. Created Message Service API Server
2. Contanarized the application
3. Implemented basic error handling and logging in Application
4. Used a database - MySQL
5. Can use any programming language of choice - preferable is Go/Python.
6. Achieved 0 downtime deployments (along with fluentd sidecar)
7. Deployed a database using statefulset along with a storage to achieve persisting data.

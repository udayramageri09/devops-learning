# Exercise 01 — Kubernetes Basics with Nginx

## Objective
Deploy an Nginx web server on a local Kubernetes cluster using
Minikube and kubectl, expose it through a Service, and access it
from a browser.

## Tools
- Windows 11
- Docker Desktop
- Minikube v1.39.0
- kubectl v1.37.1
- Kubernetes v1.37.0

## Procedure

1. Start Minikube:

   minikube start --driver=docker --cpus=2 --memory=3072

2. Verify the cluster:

   kubectl get nodes

3. Deploy Nginx using the manifests:

   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml

4. Verify the resources:

   kubectl get deployments
   kubectl get pods
   kubectl get services

5. Access Nginx:

   kubectl port-forward service/nginx-deployment 8080:80

6. Open http://localhost:8080 in a browser.

## Verification

- Minikube node reached Ready status.
- Nginx Deployment reported 1/1 available.
- Nginx Pod reported Running with 0 restarts.
- NodePort Service was created successfully.
- Browser displayed "Welcome to nginx!" using localhost:8080.

## Troubleshooting

Problem:
Accessing Minikube IP 192.168.49.2 timed out in the Windows browser.

Solution:
Used kubectl port-forward to access the Kubernetes Service
through localhost:8080.

## Result

Successfully deployed Nginx on Kubernetes using Minikube,
verified the running Pod and Service, and accessed the
application in a web browser.

# DevOps Lab Progress

## Exercise 01 — Kubernetes Basics with Nginx
Date: 19 October 2026
Status: Completed and verified

### Implementation
- Installed WSL 2 and Ubuntu.
- Installed and verified Docker Desktop.
- Installed kubectl v1.37.1 and Minikube v1.39.0.
- Started a single-node Kubernetes v1.37.0 cluster.
- Created an Nginx Deployment with one replica.
- Exposed Nginx using a NodePort Service.
- Created reusable Deployment and Service YAML manifests.

### Verification
- Kubernetes node: Ready
- Deployment: 1/1 available
- Pod: Running, 0 restarts
- Service: NodePort, port 80
- Browser: Welcome to nginx! displayed successfully

### Troubleshooting
1. Minikube IP 192.168.49.2 timed out from Windows.
   Solution: kubectl port-forward service/nginx-deployment 8080:80

2. Deployment selector was immutable.
   Solution: Matched the YAML selector to the existing app=nginx-deployment label.

3. kubectl was not recognized in a new PowerShell terminal.
   Solution: Added C:\DevOpsTools to PATH.

### Next
Exercise 02 — Flask Application on Minikube.

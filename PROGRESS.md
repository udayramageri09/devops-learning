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

## Exercise 02 — Flask Application on Minikube
Date: 19 October 2026
Status: Completed and verified

### Implementation
- Created a Python Flask application.
- Created requirements.txt and Dockerfile.
- Built the flask-minikube:v1 Docker image.
- Loaded the image into Minikube.
- Created a Kubernetes Deployment with imagePullPolicy: Never.
- Exposed Flask using a NodePort Service on port 15000.
- Configured an HTTP readiness probe.

### Verification
- Flask Pod: 1/1 Running
- Container restarts: 0
- Home endpoint: HTTP 200 OK
- Health endpoint: HTTP 200 OK

### Next
Exercise 03 — Flask ReplicaSet Scaling and Self-Healing.

## Exercise 03 — ReplicaSet Scaling and Self-Healing
Date: 19 October 2026
Status: Completed and verified

- Deployed Flask using a Kubernetes ReplicaSet.
- Scaled from 3 to 5 replicas.
- Configured readiness and liveness probes.
- Deleted one Pod to demonstrate self-healing.
- Kubernetes automatically created a replacement.
- Verified five running Pods with zero restarts.

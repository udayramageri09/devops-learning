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

## Exercise 04 — Docker Networking
Date: 19 October 2026
Status: Completed and verified

- Created the devops-lab-network custom bridge network.
- Started MySQL and Redis containers.
- Built a Dockerized Flask application.
- Connected Flask to MySQL and Redis using container hostnames.
- Verified /check returned HTTP 200 OK.
- Verified both MySQL and Redis reported connected.

## Exercise 05 — Docker Security and Python Docker SDK
Date: 19 October 2026
Status: Partially completed — Docker SDK verified; AppArmor unavailable

### Verified
- Connected Python Docker SDK to Docker Engine 29.8.2.
- Listed containers.
- Created and executed a temporary Alpine container.
- Confirmed exit code 0.
- Retrieved logs and removed the container.
- Inspected Docker security options.

### Environment Limitation
- Docker reported seccomp and cgroupns, but not AppArmor.
- WSL Ubuntu reported that the AppArmor filesystem was not mounted.
- Custom AppArmor profile enforcement was not demonstrated.
- Included an illustrative AppArmor profile for reference.

## Exercise 06 — Monitoring and Alerting
Date: 19 October 2026
Status: Monitoring and Grafana alert verified; Jenkins integration pending

- Created a Flask application exposing Prometheus metrics.
- Implemented request counter and active-user gauge.
- Configured Prometheus scraping.
- Connected Grafana to Prometheus.
- Created dashboard panels for monitoring metrics.
- Configured an alert when active users exceed 80.
- Triggered the alert with active_users = 95.
- Verified Grafana displayed 1 firing alert.
- Jenkins integration remains pending.

## Exercise 07 — Jenkins Installation and CI/CD
Date: 19 October 2026
Status: Completed and verified

- Installed Jenkins LTS using Docker.
- Configured Jenkins on localhost:8081.
- Created Freestyle job devops-hello-world.
- Executed shell commands.
- Verified build #1 finished with SUCCESS.

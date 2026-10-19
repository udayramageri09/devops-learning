# DevOps Lab — Troubleshooting Guide

## 1. Docker Command Not Found
Check Docker Desktop installation and ensure Docker CLI is on PATH.

docker version
docker info

## 2. Docker Daemon Not Running
Start Docker Desktop and wait for the engine to become available.

docker ps

## 3. Minikube Not Running
Check cluster status and start it if necessary.

minikube status
minikube start --driver=docker

## 4. Kubernetes Pod Not Running
Inspect Pod status, events and logs.

kubectl get pods -o wide
kubectl describe pod POD_NAME
kubectl logs POD_NAME

## 5. Deployment Not Ready
Inspect rollout progress and available resources.

kubectl rollout status deployment/DEPLOYMENT_NAME
kubectl get events --sort-by=.metadata.creationTimestamp

## 6. Jenkins Cannot Access GitHub
Verify the repository URL, branch and network access.
Check whether credentials are required for private repositories.

## 7. Jenkins Pipeline: No Such DSL Method 'pipeline'
A UTF-8 Byte Order Mark may be present at the beginning
of the Jenkinsfile. Save it using UTF-8 without BOM.

## 8. Python Not Found in Jenkins
The official Jenkins image may not contain Python.
For the lab, Python was installed inside the running container.
A custom Jenkins image is preferable for reproducibility.

## 9. Flask Health Check Fails
Check whether the application process started successfully,
which port it uses and whether its dependencies are installed.

## 10. Prometheus Target Down
Verify that Prometheus and the application share a network,
the application exposes /metrics, and the scrape target is correct.

## 11. Grafana Alert Not Firing
Check the query, threshold, evaluation interval and
whether the metric actually crosses the configured threshold.

## 12. Kubectl Cannot Attach to a Short-Lived Test Pod
A fast-running container may exit before kubectl attaches.
If the command output reports HTTP 200, the connectivity
test may still have completed successfully.

## 13. Multinode Cluster Has a NotReady Worker
New workers can take time to initialize.

kubectl get nodes
kubectl wait --for=condition=Ready node/minikube-m03 --timeout=180s

## 14. Git Line Ending Warnings
LF/CRLF warnings are common when using Git on Windows.
Review changes before committing; these warnings alone
do not necessarily indicate a problem.

## 15. Git Push Rejected
Check the branch and remote status.

git status
git remote -v
git pull --rebase origin main

Resolve conflicts carefully before pushing again.

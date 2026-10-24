# DevOps Lab — Faculty Evaluation Preparation

## Repository
https://github.com/udayramageri09/devops-learning

## Demonstrated Exercises

| No. | Exercise | Evidence |
|-----|----------|----------|
| 01 | Kubernetes Deployment and Service | Nginx deployment and NodePort Service |
| 02 | Flask on Minikube | Docker image, Kubernetes deployment, health endpoint |
| 03 | ReplicaSet | Scaling and automatic Pod replacement |
| 04 | Docker Networking | Flask communication with MySQL and Redis |
| 05 | Docker Security | Security inspection and Docker Python SDK |
| 06 | Monitoring | Prometheus metrics, Grafana dashboard, firing alert |
| 07 | Jenkins | Successful Freestyle build |
| 08 | Jenkins and GitHub | Successful manual build and automatic SCM polling build; no webhook |
| 09 | Jenkins Pipeline | Five-stage pipeline SUCCESS on main; 2 Flask unit tests passed; health check successful |
| 10 | Multinode Kubernetes | Three Ready nodes, five Pods, Service HTTP 200 |

## Exercise 09 — Latest Verified Pipeline

- Jenkins job: devops-python-pipeline
- GitHub branch: main
- Verified Git commit: 2a99f23f442d5f511a58aa9457b5934f171af6c0
- Successful stages: Build, Test, Deploy, Run Application, Test Application
- Unit tests: test_health and test_home both passed (2/2).
- Health endpoint: http://localhost:15000/health
- Health response: {"status":"healthy"}
- Final Jenkins console result: Finished: SUCCESS
- Deployment scope: Local to the Jenkins container.
## Important Demonstration Commands

docker ps
docker network ls
minikube status
kubectl get nodes -o wide
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl get replicasets
git log --oneline -10
git status

## Demonstration URLs

- Jenkins: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

These URLs require the corresponding local containers to be running.

## Known Limitations

- AppArmor enforcement was not demonstrated in the WSL environment.
- Jenkins GitHub integration was verified using both manual builds and automatic SCM polling; GitHub webhook triggering was not configured.
- Exercise 09 deploys locally inside Jenkins, not to production. Its test stage runs two Flask unit tests; broader automated testing is not included.
- Exercise 10 uses Nginx demonstration workloads.
- Minikube registry was enabled, but image push and pull were not tested.

## Evaluation Preparation

Before demonstrating:
1. Start Docker Desktop.
2. Verify required Docker containers.
3. Verify Minikube cluster status.
4. Check Kubernetes Pods and Deployments.
5. Open Jenkins and inspect successful builds.
6. Open Grafana and Prometheus.
7. Explain each exercise's objective, commands and observed result.

Note: This document is a preparation checklist, not an official
interpretation of faculty evaluation criteria.

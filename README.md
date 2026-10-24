# DevOps Learning and Lab Manual

This repository contains the implementation and documentation of 10 DevOps laboratory exercises.

## Technologies
- Git and GitHub
- Docker and Docker Compose concepts
- Kubernetes and Minikube
- Python and Flask
- MySQL and Redis
- Prometheus and Grafana
- Jenkins CI/CD
- Linux and WSL2

## Laboratory Exercises

| No. | Exercise | Status |
|-----|----------|--------|
| 01 | Kubernetes Deployment and Service | Completed |
| 02 | Dockerized Flask on Minikube | Completed |
| 03 | ReplicaSet Scaling and Self-Healing | Completed |
| 04 | Docker Networking with MySQL and Redis | Completed |
| 05 | Docker Security and Python SDK | Partially completed (AppArmor limitation) |
| 06 | Prometheus and Grafana Monitoring | Completed |
| 07 | Jenkins Installation and CI Job | Completed |
| 08 | Jenkins and GitHub Integration | Completed |
| 09 | Jenkins Multistage Pipeline | Completed |
| 10 | Multinode Kubernetes | Completed |

## Verification Highlights

- Flask applications tested using HTTP requests.
- ReplicaSet scaling and self-healing demonstrated.
- Docker container connectivity to MySQL and Redis verified.
- Docker Python SDK successfully managed containers; the built-in Seccomp profile was verified.
- Prometheus collected application metrics.
- Grafana alert entered the Firing state.
- Jenkins Freestyle jobs completed successfully, including an automatic SCM polling build.
- Jenkins five-stage pipeline executed successfully, with two Flask unit tests passing and a successful health check.
- Three-node Minikube cluster reached Ready status.
- Product Catalog: 2/2 replicas Ready.
- Shopping Cart: 3/3 replicas Ready.
- Both Kubernetes services returned HTTP 200.

## Evaluation Preparation

- [Faculty Evaluation Guide](FACULTY_EVALUATION.md)
- [Revision Notes](REVISION.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Progress Tracker](PROGRESS.md)
- [Roadmap](ROADMAP.md)

## Important Notes

- AppArmor was disabled in the tested WSL2 kernel; custom AppArmor enforcement was not demonstrated. Exercise 05 remains partially completed.
- Jenkins GitHub integration was verified with manual builds and automatic SCM polling; GitHub webhooks were not configured.
- Product Catalog and Shopping Cart are demonstration Nginx workloads.
- Grafana dashboards and alerts were configured through the Grafana interface.

## Repository Structure

Each exercise has its own directory containing the available source code,
configuration files, Kubernetes manifests, Jenkinsfile, and/or README documentation.

## Conclusion

All 10 laboratory exercises have been documented, with implementation
results, verification, and known limitations recorded.

# DevOps Engineering Laboratory Portfolio & Manual

This repository contains the implementation, architecture, automated testing, and verification documentation for a comprehensive 10-exercise DevOps curriculum. Designed for college evaluation and portfolio presentation, all laboratory exercises emphasize reproducible infrastructure, automation, security principles, and practical diagnostics.

---

## Technology Stack

- **Containerization:** Docker Desktop, Docker Engine `v29.8.2`, Docker Compose `v2`, Docker Python SDK `v7.1.0`
- **Container Orchestration:** Kubernetes `v1.37.0`, Minikube `v1.39.0` (Multi-node Docker driver)
- **Application Services:** Python `3.12` / `3.13`, Flask `v3.1.1`, Gunicorn, Nginx `1.27-alpine`
- **Databases & Caches:** MySQL `8.4 LTS`, Redis `7-alpine`
- **Continuous Integration & Delivery:** Jenkins LTS, Declarative & Freestyle Pipelines, Git SCM Polling
- **Observability & Alerting:** Prometheus, Grafana, `prometheus_client` Python SDK
- **Security & Linux Internals:** AppArmor MAC profile design & syntax verification, Linux Seccomp syscall filtering, Linux DAC unprivileged execution (`appuser`), WSL2 Ubuntu

---

## Laboratory Completion Matrix

| No. | Lab Topic | Status | Key Deliverables & Evidence |
|:---:|:---|:---:|:---|
| **01** | Kubernetes Deployment & Service | **Completed** | Nginx Deployment (`1/1`), NodePort Service, HTTP 200 via `kubectl port-forward` |
| **02** | Dockerized Flask on Minikube | **Completed** | Custom Docker image `flask-minikube:v1`, Kubernetes NodePort Service, health probes |
| **03** | ReplicaSet Scaling & Self-Healing | **Completed** | Scale from 3 to 5 replicas; automatic Pod recreation upon deletion verified on multi-node cluster |
| **04** | Docker Networking & Multi-Service Compose | **Completed** | Custom bridge network `devops-lab-network`; Flask communication with MySQL and Redis |
| **05** | Docker Security, Hardening & Python SDK | **Partially Completed** | Hardened non-root Dockerfile (UID 999), AppArmor profile syntax valid, Seccomp verified, Docker SDK demo. *(Enforcement unavailable in WSL2)* |
| **06** | Prometheus & Grafana Monitoring | **Completed** | Flask `/metrics` endpoint, Prometheus scrape targets, Grafana dashboard, firing alert at active users = 95 |
| **07** | Jenkins Installation & Freestyle CI | **Completed** | Jenkins LTS running on Docker with persistent volume `jenkins_home`; Build #1 SUCCESS |
| **08** | Jenkins & GitHub CI Integration | **Completed** | Git SCM integration on `main`; verified manual build #1 and automatic SCM polling build #2 |
| **09** | Jenkins Multi-Stage Declarative Pipeline | **Completed** | 5-stage declarative pipeline (`Build`, `Test`, `Deploy`, `Run`, `Test`); Flask unit tests passing; health check HTTP 200 |
| **10** | Multi-Node Kubernetes Orchestration | **Completed** | 3-node cluster (`minikube`, `minikube-m02`, `minikube-m03`); pod anti-affinity; 5 replicas running with HTTP 200 |

---

## Verification & Key Highlights

- **Flask Microservices:** Tested through HTTP requests and isolated Python `unittest` suites.
- **Self-Healing Pods:** Demonstrated ReplicaSet healing across cluster nodes when individual pods are terminated.
- **Container Networking:** Demonstrated DNS resolution and multi-tier connectivity across isolated bridge networks without publishing internal database ports.
- **Container Hardening:** Demonstrated unprivileged container execution (`UID 999 appuser`), bytecode suppression, and Seccomp filtering (`Seccomp: 2`).
- **Monitoring & Alerting:** Real-time metrics scraped by Prometheus; threshold-based Grafana alert successfully triggered into `Firing` state.
- **CI/CD Automation:** Jenkins Freestyle jobs with SCM polling and full 5-stage Declarative Pipeline executing build, test discovery, background process orchestration, and post-build cleanup.
- **Multi-Node Scheduling:** Pod anti-affinity distribution verified across control-plane and worker nodes.

---

## Repository Structure

```text
devops-learning/
├── .github/
│   └── workflows/              # GitHub Actions CI for automated test & lint verification
├── exercise-01-kubernetes/      # Single-node Kubernetes deployment and service manifests
├── exercise-02-minikube-flask/  # Flask microservice container and Kubernetes configuration
├── exercise-03-replicaset/      # ReplicaSet scaling and multi-node self-healing manifests
├── exercise-04-docker-networking/# Flask, MySQL 8.4, and Redis 7 multi-container composition
├── exercise-05-docker-security/ # AppArmor MAC profile, Seccomp tests, Docker SDK automation
├── exercise-06-monitoring/      # Flask Prometheus metrics app, scrape config, Grafana dashboard
├── exercise-07-jenkins/         # Jenkins LTS Docker deployment with persistent storage
├── exercise-08-jenkins-github/  # Jenkins SCM integration and automatic polling verification
├── exercise-09-jenkins-pipeline/# Declarative Jenkinsfile with 5 automated stages
├── exercise-10-multinode-kubernetes/# 3-node Minikube cluster with pod anti-affinity workloads
├── foundations/                 # Linux process management and command fundamentals
├── FACULTY_EVALUATION.md        # Comprehensive evaluation checklist and demonstration commands
├── PROGRESS.md                  # Chronological implementation logs and milestones
├── REVISION.md                  # Quick revision notes and viva voce Q&A
├── ROADMAP.md                   # Lab progression roadmap and future improvements
└── TROUBLESHOOTING.md           # Practical issues encountered and resolutions
```

---

## Reproducible Local Verification

To run verification commands in Windows PowerShell:

### 1. Python Unit Tests (Exercises 02 and 05)
```powershell
py -m unittest discover -s exercise-02-minikube-flask -p "test_*.py" -v
py -m unittest discover -s exercise-05-docker-security -p "test_*.py" -v
```

### 2. Exercise 05 Security & Docker SDK Harness
```powershell
py .\exercise-05-docker-security\apply_apparmor.py
py .\exercise-05-docker-security\test_restricted_actions.py
py .\exercise-05-docker-security\docker_sdk_demo.py
```

### 3. Kubernetes & Cluster Status
```powershell
kubectl get nodes -o wide
kubectl get deployments,replicasets,pods -o wide
kubectl get services
```

### 4. Running Infrastructure Check
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## Known Environment Limitations

1. **Custom AppArmor Enforcement:** The WSL2 Linux kernel in the local testing environment (`6.18.54.1-microsoft-standard-WSL2`) disables AppArmor (`/sys/module/apparmor/parameters/enabled: N`). While the `devops-lab-profile` passed syntax validation (`apparmor_parser -Q`), custom enforcement cannot be active without an AppArmor-enabled Linux host. Exercise 05 is therefore designated **Partially Completed**.
2. **Jenkins Webhooks vs. Polling:** Jenkins GitHub integration was tested and verified using scheduled SCM polling (`H/5 * * * *`) rather than external webhooks, as the Jenkins server was hosted on an internal localhost environment without a public tunnel.
3. **Multi-Node Workloads:** The multi-node workloads deployed in Exercise 10 utilize Nginx demonstration images configured with resource limits and pod anti-affinity rules.

---

## Documentation & Evaluation References

- [Faculty Evaluation Guide](FACULTY_EVALUATION.md) — Step-by-step checklist and commands for academic evaluators
- [Revision & Viva Guide](REVISION.md) — Conceptual questions, definitions, and command summaries
- [Troubleshooting Reference](TROUBLESHOOTING.md) — Solutions for common Docker, Kubernetes, and Jenkins issues
- [Progress Log](PROGRESS.md) — Detailed chronological log of all laboratory milestones
- [Curriculum Roadmap](ROADMAP.md) — Architectural phases and roadmap

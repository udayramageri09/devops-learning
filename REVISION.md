# DevOps Lab — Quick Revision and Viva Questions

## Docker

Q: What is Docker?
A: A platform for building and running applications in containers.

Q: What is the difference between an image and a container?
A: An image is a packaged template; a container is a running instance.

Q: What is a Docker bridge network?
A: A network allowing containers to communicate using container names.

Q: What is the purpose of Docker volumes?
A: To persist data independently of container lifecycle.

## Container Security

Q: What is the difference between DAC and MAC in Linux?
A: DAC (Discretionary Access Control) enforces permissions based on user identity and file modes (e.g. non-root UID 999). MAC (Mandatory Access Control, like AppArmor) enforces centralized kernel policies on programs regardless of user privileges.

Q: Why should containers run as a non-root user?
A: Running as an unprivileged user prevents an attacker from immediately possessing root capabilities if an application vulnerability is compromised.

Q: What is Seccomp?
A: Secure Computing Mode, a Linux kernel facility that filters and restricts the system calls (syscalls) accessible to a container process.

Q: What is AppArmor?
A: A Linux Security Module (LSM) that confines programs to specific filesystem paths, network operations, and POSIX capabilities using security profiles.


## Kubernetes

Q: What is a Pod?
A: The smallest deployable Kubernetes unit, containing one or more containers.

Q: What is a Deployment?
A: A controller that manages desired application replicas and rolling updates.

Q: What is a ReplicaSet?
A: A controller that maintains the specified number of Pod replicas.

Q: What is a Service?
A: A stable networking abstraction for accessing selected Pods.

Q: What is NodePort?
A: A Service type exposing a port on Kubernetes nodes.

Q: What is Minikube?
A: A tool for running a local Kubernetes cluster.

Q: What is pod anti-affinity?
A: A scheduling rule that discourages or prevents selected Pods from sharing a topology domain.

Q: What is the difference between preferred and required anti-affinity?
A: Preferred influences scheduling; required must be satisfied.

## Jenkins

Q: What is Jenkins?
A: An automation server commonly used for CI/CD.

Q: What is CI?
A: Continuous Integration, automatically integrating and validating code changes.

Q: What is CD?
A: Continuous Delivery or Continuous Deployment, depending on the workflow.

Q: What is a Jenkinsfile?
A: A file defining a Jenkins Pipeline as code.

Q: What are Pipeline stages?
A: Logical sections such as Build, Test and Deploy.

Q: What is a Freestyle job?
A: A Jenkins job configured through the user interface.

## Monitoring

Q: What is Prometheus?
A: A monitoring system that collects and queries time-series metrics.

Q: What is Grafana?
A: A platform for visualizing data and configuring alerts.

Q: What is a metrics endpoint?
A: An HTTP endpoint exposing measurements for monitoring systems.

Q: What is an alert rule?
A: A condition that determines when monitoring data should trigger an alert.

## Git

Q: What does git add do?
A: Stages changes for a commit.

Q: What does git commit do?
A: Records staged changes in local repository history.

Q: What does git push do?
A: Uploads local commits to a remote repository.

## Important Commands

docker ps
docker images
docker logs CONTAINER_NAME
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get nodes
kubectl describe pod POD_NAME
kubectl logs POD_NAME
kubectl apply -f FILE.yaml
kubectl rollout status deployment/NAME
git status
git add .
git commit -m "message"
git push origin main

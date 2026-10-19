# Exercise 03 — Kubernetes ReplicaSet Scaling and Self-Healing

## Objective
Deploy a flash-sale Flask application using a Kubernetes ReplicaSet,
scale from 3 to 5 replicas, and demonstrate automatic Pod replacement.

## Technologies
Docker, Flask, Kubernetes, Minikube, kubectl

## Procedure

### Deploy 3 replicas
kubectl apply -f .\exercise-03-replicaset\replicaset.yaml
kubectl get pods -l app=flash-sale

### Scale to 5 replicas
kubectl scale replicaset flash-sale-replicaset --replicas=5
kubectl get replicaset flash-sale-replicaset
kubectl get pods -l app=flash-sale

### Test self-healing
$podToDelete = kubectl get pods -l app=flash-sale -o jsonpath='{.items[0].metadata.name}'
kubectl delete pod $podToDelete
kubectl get pods -l app=flash-sale -w

Press Ctrl+C to stop watching.

## Verification Results
- Initial replicas: 3
- Scaled replicas: 5
- Deleted Pod: flash-sale-replicaset-2k8px
- Replacement Pod observed: flash-sale-replicaset-6kctm
- Final state: 5/5 Pods running
- Container restarts: 0
- Readiness probe: /health
- Liveness probe: /health

## Key Concepts
A ReplicaSet maintains the desired number of Pod replicas.
Scaling increases or decreases the desired replica count.
Self-healing occurs when Kubernetes replaces a deleted Pod.
Readiness probes determine whether Pods can receive traffic.
Liveness probes help Kubernetes detect unhealthy containers.

## Result
Successfully demonstrated ReplicaSet scaling and automatic
Pod replacement in a local Minikube cluster.

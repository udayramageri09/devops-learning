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

* Initial replicas: 3
* Scaled replicas: 5
* Deleted Pod: flash-sale-replicaset-2k8px
* Replacement Pod observed: flash-sale-replicaset-6kctm
* Final state: 5/5 Pods running
* Container restarts: 0
* Readiness probe: /health
* Liveness probe: /health

## Key Concepts

A ReplicaSet maintains the desired number of Pod replicas.
Scaling increases or decreases the desired replica count.
Self-healing occurs when Kubernetes replaces a deleted Pod.
Readiness probes determine whether Pods can receive traffic.
Liveness probes help Kubernetes detect unhealthy containers.

## Result

Successfully demonstrated ReplicaSet scaling and automatic
Pod replacement in a local Minikube cluster.

## Additional Self-Healing Verification — Multi-Node Cluster

A second self-healing test was performed on the three-node Minikube cluster.

### Test Procedure

```powershell

$podToDelete = kubectl get pods -l app=flash-sale -o jsonpath='{.items[0].metadata.name}'

kubectl delete pod $podToDelete

kubectl get pods -l app=flash-sale -o wide

```

### Initial Results

- Deleted pod: `flash-sale-replicaset-6kctm`

- Replacement pod: `flash-sale-replicaset-t2xnb`

- Replacement scheduled on: `minikube-m02`

- Initial replacement status: `ErrImageNeverPull`

- Image: `flask-minikube:v1`

- Image pull policy: `Never`

Kubernetes successfully created a replacement pod, but the worker node did not initially have the required locally built image.

### Troubleshooting and Resolution

The pod events reported:

```text

Container image "flask-minikube:v1" is not present with pull policy of Never

```

Confirmed that the image existed on the original Minikube node, then loaded it into the cluster:

```powershell

minikube image load flask-minikube:v1

```

### Final Verification

```powershell

kubectl get pods -l app=flash-sale -o wide

kubectl get replicaset flash-sale-replicaset

```

Observed results:

- Desired replicas: **5**

- Current replicas: **5**

- Ready replicas: **5**

- Replacement pod `flash-sale-replicaset-t2xnb`: **1/1 Running**

- Replacement node: `minikube-m02`

- Replacement container restarts: **0**

### Learning Outcome

ReplicaSets automatically replace deleted pods to maintain the desired replica count. However, successful recovery also depends on the required container image being available on the node where a replacement pod is scheduled.

**Final Result: Self-healing successfully verified with 5/5 replicas ready.**


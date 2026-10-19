# Exercise 01 — Kubernetes Basics with Nginx

## Objective

Deploy an Nginx web server on a local Kubernetes cluster using Minikube and kubectl, expose it through a Service, and access it from a browser.

## Tools and Environment

- Windows 11 and PowerShell
- Docker Desktop
- Minikube v1.39.0
- kubectl v1.37.1
- Kubernetes v1.37.0
- Docker driver

## Kubernetes Resources

| Resource | Name | Configuration |
|---|---|---|
| Deployment | `nginx-deployment` | 1 replica, `nginx:stable` |
| Service | `nginx-deployment` | NodePort, port 80 to container port 80 |

The Service selector `app: nginx-deployment` matches the Pod labels in `deployment.yaml`.

## Procedure

Run the following commands from the repository root in PowerShell.

### 1. Start Minikube

```powershell
minikube start --driver=docker --cpus=2 --memory=3072
```

If Minikube is already running, this step is unnecessary.

### 2. Verify the cluster

```powershell
kubectl get nodes
```

### 3. Apply the manifests

```powershell
kubectl apply -f .\exercise-01-kubernetes\deployment.yaml
kubectl apply -f .\exercise-01-kubernetes\service.yaml
```

### 4. Verify the rollout and resources

```powershell
kubectl rollout status deployment/nginx-deployment --timeout=120s
kubectl get deployment nginx-deployment
kubectl get pods -l app=nginx-deployment
kubectl get service nginx-deployment
```

### 5. Access Nginx in a browser

In a separate PowerShell terminal, run:

```powershell
kubectl port-forward service/nginx-deployment 8080:80
```

Keep that terminal open, then visit <http://localhost:8080>. Stop port forwarding with `Ctrl+C` when finished.

## Verification

The initial exercise verified:

- Minikube reached `Ready` status.
- The Nginx Deployment had 1/1 available replicas.
- The Nginx Pod was `Running` with 0 restarts at the time of that check.
- A NodePort Service was created.
- The browser displayed **Welcome to nginx!** through `http://localhost:8080`.

### Follow-up deployment verification — October 19, 2026

Reapplying both manifests returned `unchanged`. The rollout completed successfully:

```text
deployment.apps/nginx-deployment unchanged
service/nginx-deployment unchanged
deployment "nginx-deployment" successfully rolled out
```

The Deployment reported 1/1 ready, up-to-date, and available replicas. The Service was `NodePort` with ClusterIP `10.105.81.48` and port mapping `80:32322/TCP`. These are observed cluster values and can change when resources are recreated.

## Troubleshooting

**Problem:** Accessing the Minikube IP (`192.168.49.2`) timed out in the Windows browser.

**Solution:** Use `kubectl port-forward` to reach the Kubernetes Service through `localhost:8080` instead of relying on direct access to the Minikube node IP.

## Optional Cleanup

Only if you want to remove the resources created for this exercise:

```powershell
kubectl delete -f .\exercise-01-kubernetes\service.yaml
kubectl delete -f .\exercise-01-kubernetes\deployment.yaml
```

These commands remove the named Nginx Service and Deployment. They do not stop Minikube or delete resources belonging to other exercises.

## Result

Successfully deployed and exposed Nginx using Minikube and Kubernetes, verified the Deployment and Service, accessed Nginx in a browser, and confirmed a successful Deployment rollout.

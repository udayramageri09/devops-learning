# Exercise 10 — Multinode Kubernetes Cluster

## Objective

Create a three-node Kubernetes cluster using Minikube,
enable the registry addon, and deploy applications using
multiple replicas and pod anti-affinity.

## Environment

* Minikube with Docker driver
* Kubernetes v1.37.0
* Container runtime: containerd
* Three nodes:

  * minikube (control plane)
  * minikube-m02 (worker)
  * minikube-m03 (worker)

## Cluster Setup

Added two worker nodes to the existing Minikube cluster:

minikube node add --worker
minikube node add --worker

Verified all three nodes were Ready:

kubectl get nodes -o wide

## Registry Addon

Enabled the local registry addon:

minikube addons enable registry

Verified the addon was enabled and the registry and
registry-proxy Pods were running.

Note: The registry addon was enabled and verified,
but no custom image was pushed to it.

## Application Deployments

### Product Catalog

* Deployment: product-catalog
* Replicas: 2
* Container image: nginx:1.27-alpine
* Service: product-catalog-service
* Service type: ClusterIP

### Shopping Cart

* Deployment: shopping-cart
* Replicas: 3
* Container image: nginx:1.27-alpine
* Service: shopping-cart-service
* Service type: ClusterIP

Both are demonstration Nginx workloads rather than
functional e-commerce applications.

## Pod Anti-Affinity

Configured preferredDuringSchedulingIgnoredDuringExecution
using topologyKey kubernetes.io/hostname.

This encourages replicas of the same application to
run on different nodes.

## Deployment Commands

kubectl apply -f product-catalog.yaml
kubectl apply -f shopping-cart.yaml

## Verification Commands

kubectl get nodes -o wide
kubectl get deployments product-catalog shopping-cart
kubectl get pods -l app=product-catalog -o wide
kubectl get pods -l app=shopping-cart -o wide
kubectl get services product-catalog-service shopping-cart-service

## Verified Results

* All three Kubernetes nodes: Ready
* Registry addon: enabled
* Registry Pods: Running
* Product Catalog: 2/2 replicas Ready
* Shopping Cart: 3/3 replicas Ready
* Total application Pods: 5
* All application Pods: Running

- Latest observed restart count: 1 per application Pod



### Observed Pod Placement

* minikube:

  * Shopping Cart: 1
* minikube-m02:

  * Product Catalog: 1
  * Shopping Cart: 1
* minikube-m03:

  * Product Catalog: 1
  * Shopping Cart: 1

The observed placement demonstrates successful
distribution of replicas across multiple nodes.

## Result

Successfully configured a three-node Minikube cluster,
enabled its registry addon, and deployed two replicated
workloads with preferred pod anti-affinity.

## Service Connectivity Verification

Product Catalog:

* Endpoint: http://product-catalog-service
* HTTP status: 200
* Result: Passed

Shopping Cart:

* Endpoint: http://shopping-cart-service
* HTTP status: 200
* Result: Passed

Both services were successfully accessed from temporary
curl Pods running inside the Kubernetes cluster.

## Deployment Rollout Verification



Verified the successful rollout of both Kubernetes deployments.



### Commands



```bash

kubectl rollout status deployment/product-catalog --timeout=120s

kubectl rollout status deployment/shopping-cart --timeout=120s

```



### Observed Output



```text

deployment "product-catalog" successfully rolled out

deployment "shopping-cart" successfully rolled out

```



### Final Verification Summary



- All three Kubernetes nodes were `Ready`.

- Product Catalog: 2/2 replicas ready.

- Shopping Cart: 3/3 replicas ready.

- All five application Pods were running.

- Application Pods were distributed across the three nodes.

- Both deployments successfully rolled out.



The deployments use Nginx demonstration containers to verify Kubernetes multi-node scheduling and replica availability, rather than functional e-commerce applications.


# Exercise 02 — Dockerized Flask on Minikube

## Objective
Build a Flask Docker image and deploy it to Minikube.

## Steps
1. Build: docker build -t flask-minikube:v1 .\exercise-02-minikube-flask
2. Load: minikube image load flask-minikube:v1
3. Deploy: kubectl apply -f .\exercise-02-minikube-flask\deployment.yaml
4. Service: kubectl apply -f .\exercise-02-minikube-flask\service.yaml
5. Access: kubectl port-forward service/flask-service 15000:15000

## Verification
- Flask Pod: 1/1 Running
- Home endpoint: HTTP 200 OK
- Health endpoint: HTTP 200 OK

## Result
Successfully containerized and deployed Flask on Kubernetes.

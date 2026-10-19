# Exercise 06 — Monitoring and Alerting

## Objective
Monitor a Python Flask application using Prometheus and Grafana,
visualize metrics, and demonstrate threshold-based alerting.

## Technologies
Python, Flask, Prometheus Client, Docker, Prometheus, Grafana

## Components
- app.py: Flask application exposing Prometheus metrics
- requirements.txt: Python dependencies
- Dockerfile: Container image
- prometheus.yml: Prometheus scrape configuration

## Metrics
- lab_http_requests_total: HTTP request counter
- lab_active_users: Simulated active-user gauge

## Procedure
1. Build the Flask monitoring image.
2. Run Flask on the devops-lab-network bridge network.
3. Configure Prometheus to scrape lab-monitoring-app:8000.
4. Start Prometheus on port 9090.
5. Start Grafana on port 3000.
6. Connect Grafana to Prometheus.
7. Create panels for HTTP requests and active users.
8. Configure a Grafana alert for active users above 80.
9. Set active users to 95 to test the alert.
10. Restore random user simulation.

## Verification
- Flask application: HTTP 200 OK
- /simulate endpoint: HTTP 200 OK
- /metrics endpoint: Working
- Prometheus collected HTTP request and active-user metrics
- Grafana displayed changing metric values
- Alert folder: DevOps Lab Alerts
- Evaluation group: devops-monitoring-group
- Evaluation interval: 1 minute
- Alert threshold: Active users above 80
- Alert test value: 95
- Grafana alert state: Firing (verified)

## Jenkins Integration
Jenkins integration was not implemented in this exercise.
Jenkins is covered separately in Exercises 07–09.

## Result
Successfully demonstrated Python application monitoring with
Prometheus and Grafana, including a firing threshold alert.

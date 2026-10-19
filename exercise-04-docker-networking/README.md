# Exercise 04 — Docker Networking

## Objective
Create a custom Docker bridge network and establish communication
between Flask, MySQL, and Redis containers.

## Technologies
Docker, Python, Flask, MySQL 8.4, Redis 7

## Files
- app.py: Flask application with database and cache checks
- requirements.txt: Python dependencies
- Dockerfile: Flask container image

## Procedure

### Create the bridge network
docker network create devops-lab-network

### Start MySQL
docker run -d --name lab-mysql --network devops-lab-network -e MYSQL_ROOT_PASSWORD=labroot123 -e MYSQL_DATABASE=devops_lab mysql:8.4

### Start Redis
docker run -d --name lab-redis --network devops-lab-network redis:7-alpine

### Build Flask image
docker build -t devops-network-flask:v1 .\exercise-04-docker-networking

### Start Flask
Run Flask on devops-lab-network, publish host port 5000,
and supply MYSQL_HOST, REDIS_HOST, and MYSQL_PASSWORD as
environment variables.

### Verify communication
docker ps
docker network inspect devops-lab-network
curl.exe -i http://localhost:5000/check

## Verified Results
- Flask endpoint: HTTP 200 OK
- MySQL connection: connected
- Redis connection: connected
- Custom bridge network: devops-lab-network
- All three containers communicate through container names

## Important Concepts
- A custom bridge network enables communication between containers.
- Docker provides name resolution for containers on user-defined networks.
- Flask connects to MySQL using the hostname lab-mysql.
- Flask connects to Redis using the hostname lab-redis.
- MySQL and Redis do not require published host ports for internal access.
- Environment variables can supply runtime configuration.
- Real production passwords should be managed using secrets.

## Result
Successfully demonstrated Docker networking between three containers.

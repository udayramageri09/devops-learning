# Exercise 05 — Docker Security and Python Docker SDK

## Objective

Study Docker container security using AppArmor and manage Docker
containers programmatically using the Python Docker SDK.

## Files

- apparmor-profile: Example AppArmor policy (not enforced)
- docker_sdk_demo.py: Docker SDK demonstration
- requirements.txt: Python dependency

## Part A — AppArmor

### Commands

docker info --format '{{json .SecurityOptions}}'
docker run --rm alpine:3.20 cat /proc/1/attr/current

### Observations

Docker security options:
- seccomp with built-in profile
- cgroup namespaces

Container security label:
- kernel

Ubuntu WSL reported:
- AppArmor module loaded
- AppArmor filesystem not mounted

### Result

AppArmor enforcement could not be demonstrated in the current
Docker Desktop and WSL2 environment.

The included AppArmor profile is an example only. It was not
loaded, validated, or enforced.

## Part B — Python Docker SDK

### Install dependencies

py -m pip install -r .\exercise-05-docker-security\requirements.txt

### Run demonstration

py .\exercise-05-docker-security\docker_sdk_demo.py

### Verified Results

- Connected to Docker Engine 29.8.2
- Listed existing containers
- Created an Alpine test container
- Executed a command successfully
- Received exit code 0
- Retrieved container logs
- Removed the temporary container

## Important Concepts

AppArmor:
Linux mandatory access control system that restricts program actions.

Seccomp:
Restricts the system calls available to processes.

Docker SDK:
Python library for communicating with the Docker Engine API.

Container isolation:
Docker uses Linux kernel features to isolate container processes.

## Conclusion

Successfully demonstrated Docker container management using Python.
Inspected the available Docker security mechanisms and documented
the AppArmor enforcement limitation.

# Exercise 09 — Jenkins Multistage CI/CD Pipeline

## Objective
Create and execute a Jenkins Declarative Pipeline with five stages:
Build, Test, Deploy, Run Application, and Test Application.

## Environment
- Jenkins LTS running in Docker
- Python 3.13.5 inside Jenkins
- Flask 3.1.1
- GitHub repository: https://github.com/udayramageri09/devops-learning
- Pipeline job: devops-python-pipeline

## Pipeline Configuration
- Job type: Pipeline
- Definition: Pipeline script from SCM
- SCM: Git
- Branch: main
- Script path: exercise-09-jenkins-pipeline/Jenkinsfile

## Pipeline Stages

### 1. Build
Created a Python virtual environment and installed Flask dependencies.

### 2. Test
Checked Python application syntax using py_compile.

### 3. Deploy
Copied the Flask application into a deployment directory.

### 4. Run Application
Started the Flask application as a background process.

### 5. Test Application
Called the HTTP health endpoint:
http://localhost:15000/health

Expected response:
{"status":"healthy"}

## Verified Results
- All five stages completed successfully.
- Flask dependencies installed.
- Python syntax check passed.
- Application started successfully.
- HTTP health check returned a healthy status.
- Jenkins final result: SUCCESS.

## Troubleshooting
The first pipeline attempt failed because the Jenkinsfile contained
a UTF-8 Byte Order Mark (BOM). Saving the Jenkinsfile as UTF-8
without BOM resolved the parsing error.

Python was also installed inside the Jenkins container because
the original Jenkins image did not contain Python.

## Limitations
- Deployment is local to the Jenkins container, not production.
- The test stage checks syntax rather than running a full test suite.
- Python installed directly in the container will not survive
  container recreation unless included in a custom image.

## Result
Successfully implemented and executed a five-stage Jenkins
Declarative CI/CD Pipeline.

# Exercise 07 — Jenkins Installation and CI/CD

## Objective
Install Jenkins, configure the initial setup, and execute a CI job.

## Environment
- Jenkins LTS running in Docker
- Jenkins URL: http://localhost:8081
- Docker volume: jenkins_home
- Job type: Freestyle project

## Procedure
1. Created the jenkins_home Docker volume.
2. Started the Jenkins container on port 8081.
3. Unlocked Jenkins and completed initial setup.
4. Created a Freestyle job named devops-hello-world.
5. Added an Execute shell build step.
6. Triggered the job using Build Now.
7. Examined the Console Output.

## Shell Commands
echo "Hello from Jenkins!"
echo "DevOps Lab Exercise 07"
echo "Build number: $BUILD_NUMBER"
date

## Verified Results
- Job name: devops-hello-world
- Build number: 1
- Console output displayed both expected messages
- Final status: SUCCESS

## Important Concepts
- Jenkins automates build, test, and deployment workflows.
- A Freestyle project executes configured build steps.
- A workspace stores files used during a build.
- BUILD_NUMBER is a Jenkins environment variable.
- Console Output records build execution details.

## Result
Successfully installed Jenkins and executed a Freestyle CI job.

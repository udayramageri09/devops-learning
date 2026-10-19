# Exercise 08 — Jenkins Integration with GitHub

## Objective
Connect Jenkins to a GitHub repository and execute a CI job.

## Repository
https://github.com/udayramageri09/devops-learning

## Jenkins Configuration
- Job name: devops-github-hello-world
- Job type: Freestyle
- Source Code Management: Git
- Branch: main
- Build step: Execute shell

## Build Commands
echo "Hello from Jenkins and GitHub!"
echo "DevOps Lab Exercise 08"
echo "Build number: $BUILD_NUMBER"
echo "Git commit: $(git rev-parse --short HEAD)"
ls -la

## Verification
- GitHub repository cloned successfully.
- Branch main checked out.
- Verified commit: f72f413
- Build number: 1
- Final result: SUCCESS

## Result
Successfully integrated Jenkins with GitHub and executed a CI job.

## Limitation
The job was triggered manually using Build Now.
Automatic GitHub webhook triggering was not tested.

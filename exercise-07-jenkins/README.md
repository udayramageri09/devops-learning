# Exercise 07 — Jenkins Installation and CI/CD

## Objective

Install Jenkins, complete its initial setup, and execute a Continuous Integration (CI) job using a Jenkins Freestyle project.

## Technologies Used

- Jenkins LTS
- Docker Desktop
- Docker volumes
- Jenkins Freestyle project
- Windows 11 and PowerShell
- Shell scripting

## Environment

| Component | Configuration |
|---|---|
| Jenkins container | `lab-jenkins` |
| Jenkins URL | `http://localhost:8081` |
| Host port | `8081` |
| Container port | `8080` |
| Agent communication port | `50000` |
| Persistent Docker volume | `jenkins_home` |
| Job type | Freestyle project |
| Job name | `devops-hello-world` |

## Procedure

### Step 1 — Create Persistent Storage

Create a Docker volume to preserve Jenkins configuration, plugins, jobs, and build history.

```powershell
docker volume create jenkins_home
```

### Step 2 — Start Jenkins

Run Jenkins LTS in a Docker container:

```powershell
docker run -d --name lab-jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

The named volume preserves Jenkins data across container restarts. The command above documents a reproducible setup; do not run it again while the existing `lab-jenkins` container is present.

### Step 3 — Complete Initial Setup

1. Open `http://localhost:8081`.
2. Retrieve the initial administrator password, if required:

   ```powershell
   docker exec lab-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

3. Unlock Jenkins and install the suggested plugins.
4. Create an administrator account and finish the setup wizard.

### Step 4 — Create a Freestyle Job

1. On the Jenkins dashboard, select **New Item**.
2. Enter `devops-hello-world` and choose **Freestyle project**.
3. Under **Build Steps**, select **Execute shell**.
4. Enter the commands below and save the job.

```bash
echo "Hello from Jenkins!"
echo "DevOps Lab Exercise 07"
echo "Build number: $BUILD_NUMBER"
date
```

### Step 5 — Execute the Job

1. Open the `devops-hello-world` job.
2. Select **Build Now**.
3. Open **Build #1** in the build history.
4. Inspect **Console Output** and the build status.

## Original Build Verification

The Freestyle job was executed and its output was inspected.

| Check | Observed result |
|---|---|
| Job name | `devops-hello-world` |
| Build number | `1` |
| Expected messages | Displayed in console output |
| Build status | `SUCCESS` |

## Additional Verification — October 19, 2026

### Container and Storage

The following PowerShell command was used:

```powershell
docker ps --filter "name=lab-jenkins" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Mounts}}"
```

Observed results:

- Container `lab-jenkins` was running.
- Host port `8081` mapped to container port `8080`.
- Port `50000` was published for Jenkins agent communication.
- The named volume `jenkins_home` was attached.

### HTTP Accessibility

The Jenkins login endpoint was checked with:

```powershell
curl.exe -s -o NUL -w "HTTP Status: %{http_code}\n" http://localhost:8081/login
```

Observed result:

```text
HTTP Status: 200
```

This confirms that the Jenkins web interface responded successfully. The container and HTTP checks do not by themselves rerun the original Freestyle build; that result is documented separately above.

## Important Concepts

- **Continuous Integration (CI):** Automates integration, build, and test workflows.
- **Jenkins:** An automation server used for CI/CD.
- **Freestyle project:** A Jenkins job configured through the web interface.
- **Docker volume:** Persistent storage for Jenkins data.
- **Workspace:** Directory used by Jenkins during a build.
- **`BUILD_NUMBER`:** Jenkins environment variable containing the current build number.
- **Console Output:** Logs showing commands, output, and build status.

## Result

Successfully configured Jenkins in Docker, executed a Freestyle CI job with a documented `SUCCESS` result, and verified that the running Jenkins container had persistent storage attached and served its login page with HTTP `200`.

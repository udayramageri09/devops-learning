# Exercise 08 — Jenkins Integration with GitHub

## Objective

Integrate Jenkins with a GitHub repository, execute a CI job, and verify both manual execution and automatic builds triggered by SCM polling.

## Repository

https://github.com/udayramageri09/devops-learning

## Tools and Technologies

- Jenkins (running locally in Docker)
- Git and GitHub
- Shell scripting
- Jenkins SCM polling

## Jenkins Configuration

| Setting | Value |
|---|---|
| Job name | `devops-github-hello-world` |
| Job type | Freestyle |
| Source Code Management | Git |
| Repository URL | `https://github.com/udayramageri09/devops-learning.git` |
| Monitored branch | `main` |
| Build step | Execute shell |
| Local Jenkins URL | `http://localhost:8081` |
| Automatic build trigger | Poll SCM |
| Polling schedule | `H/5 * * * *` |

## Build Commands

The Jenkins Freestyle job runs these shell commands:

```bash
echo "Hello from Jenkins and GitHub!"
echo "DevOps Lab Exercise 08"
echo "Build number: $BUILD_NUMBER"
echo "Git commit: $(git rev-parse --short HEAD)"
echo "Repository files:"
ls -la
```

## Part 1 — Manual Build Verification

The initial build was started manually using **Build Now**.

| Property | Verified result |
|---|---|
| Build number | **1** |
| Checked-out branch | `main` |
| Verified commit | `f72f413` |
| GitHub repository checkout | Successful |
| Final result | **SUCCESS** |

This confirmed that Jenkins could retrieve source code from GitHub and execute the configured shell commands.

## Part 2 — Automatic CI Using SCM Polling

### Configuration

In **Jenkins → Job → Configure → Build Triggers**, **Poll SCM** was enabled with this schedule:

```text
H/5 * * * *
```

Jenkins uses hash-based scheduling to check the repository approximately every five minutes. A detected commit change can automatically start a new build.

### Verification Procedure

1. Created `exercise-08-jenkins-github/polling-verification.txt` as a documentation-only change.
2. Committed and pushed the change to the `main` branch.
3. Waited for Jenkins SCM polling without selecting **Build Now**.
4. Checked the Git polling log for change detection.
5. Checked the new build's console output for its trigger, checked-out revision, shell output, and final status.

### Polling Evidence

The Git polling log reported:

```text
Last Built Revision: f72f413
Latest remote head revision on main: 59249bc
Changes found
```

### Automatic Build Results

| Property | Verified result |
|---|---|
| Test commit | `59249bc` |
| Commit message | `test(ex08): verify Jenkins SCM polling` |
| Monitored branch | `main` |
| Build number | **2** |
| Trigger | `Started by an SCM change` |
| GitHub checkout | Successful |
| Shell execution | Successful |
| Final result | **SUCCESS** |

Selected lines from the Jenkins console output:

```text
Started by an SCM change
Checking out Revision 59249bcd3066bdc02dd99d4eae2e06419a64a4a0 (refs/remotes/origin/main)
Commit message: "test(ex08): verify Jenkins SCM polling"
Hello from Jenkins and GitHub!
DevOps Lab Exercise 08
Build number: 2
Git commit: 59249bc
Finished: SUCCESS
```

## Results

Both execution methods were verified:

- **Manual build:** Jenkins checked out the GitHub repository and successfully ran the shell commands in Build #1.
- **Automatic build:** SCM polling detected the new GitHub commit and automatically triggered successful Build #2.

## Limitations

- Jenkins was hosted locally using Docker.
- Automatic triggering used **SCM polling**, not a GitHub webhook.
- GitHub webhook triggering was not configured or tested.
- This Freestyle job demonstrates Git checkout and shell execution. Flask unit tests are demonstrated separately in Exercise 09.

## Conclusion

Successfully integrated Jenkins with GitHub and verified both manual execution and automatic CI triggering through SCM polling.

**Final status: SUCCESS**

# Exercise 05 — Docker Security and Python Docker SDK

## Objective

Study Docker container security mechanisms (Seccomp and AppArmor), implement a hardened container workload, and manage Docker containers programmatically using the Python Docker SDK.

---

## Files in this Directory

- `app.py`: Lightweight Python/Flask web microservice with `/` and `/health` endpoints.
- `Dockerfile`: Hardened container definition configured with an unprivileged system user (`appuser`).
- `.dockerignore`: Excludes caches, temporary files, and backups from Docker build context.
- `apparmor-profile`: Example AppArmor Mandatory Access Control (MAC) profile (`devops-lab-profile`).
- `apply_apparmor.py`: Diagnostic and verification script checking Docker daemon security, profile syntax, and container attachment.
- `test_restricted_actions.py`: Structured test harness comparing baseline Linux DAC behavior with expected MAC security rules.
- `test_app.py`: Unit tests for the Flask microservice (`/` and `/health`).
- `docker_sdk_demo.py`: Programmatic container management demonstration using the Python Docker SDK.
- `requirements.txt`: Python dependencies (`docker==7.1.0`, `Flask==3.1.1`).
- `SECCOMP_VERIFICATION.md`: Verification logs demonstrating Docker default Seccomp syscall filtering.

---

## Security Architecture & Design

### 1. Hardened Dockerfile
Running containers as root (UID 0) presents a severe privilege-escalation risk if an application vulnerability is exploited.
The Dockerfile is hardened with:
- **Non-root user:** Creates system group `appgroup` and system user `appuser` (UID 999), executing the process without root privileges.
- **Minimal attack surface:** Built on `python:3.12-slim`.
- **Clean execution:** Sets `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` for immediate stdout/stderr streaming.
- **Restricted file ownership:** Application files are owned by `appuser:appgroup` with no write permissions to system directories.

### 2. Refined AppArmor Profile (`devops-lab-profile`)
Earlier naive rules (such as `deny /bin/** x` or `deny /usr/bin/** x` and `deny /etc/** r`) prevented the container from launching because Python, libc dynamic linkers (`/etc/ld.so.cache`), and DNS resolution (`/etc/resolv.conf`) were blocked.

The refined profile demonstrates precise Mandatory Access Control:
- **Allows Application Runtime:** Permits standard Python interpreters, shared libraries, and network stream binding for HTTP services.
- **Drops Dangerous Capabilities:** Retains `net_bind_service` but explicitly denies `sys_admin`, `sys_ptrace`, `sys_rawio`, and `sys_module`.
- **System Binary Tamper Protection:** Denies write access to `/bin/**`, `/sbin/**`, `/usr/**`, and `/lib/**`.
- **Credential Protection:** Denies all access to `/etc/shadow*`, `/etc/gshadow*`, `/etc/sudoers*`, and `/root/**`.
- **Administrative Tool Execution Denial:** Denies execution of administrative and package management tools (`/sbin/**`, `/usr/sbin/**`, `apt`, `dpkg`).

---

## Verification & Commands

### 1. Validate AppArmor Profile Syntax
The profile syntax was verified using the AppArmor parser:

```powershell
wsl apparmor_parser -Q exercise-05-docker-security/apparmor-profile
```

**Observed Result:**
- Exit code: `0`
- Result: **Syntax Valid**
- *Important note:* Syntax validation only confirms that the rules are syntactically well-formed; it does not mean the profile is loaded or enforced in the kernel.

### 2. Run AppArmor Diagnostic & Lifecycle Test
Executes `apply_apparmor.py` to evaluate the 5 security stages:

```powershell
py .\exercise-05-docker-security\apply_apparmor.py
```

**Observed Output:**
```text
============================================================
Exercise 05 — Docker AppArmor Diagnostic & Verification
============================================================

[Stage 1] Docker Engine Security Options: ['name=seccomp,profile=builtin', 'name=cgroupns']
         Docker AppArmor Support: DISABLED / UNAVAILABLE

[Stage 2] Profile Syntax Validation:
         Profile file: apparmor-profile
         Parser available: True
         Syntax valid: True
         Details: Profile syntax is valid (apparmor_parser -Q returned 0)

[Stage 3] Building image devops-ex05-apparmor:lab...
         Image build successful.

[Stage 4] Docker AppArmor unsupported; launching baseline unconfined container
         Configured SecurityOpt: []

[Stage 5] Starting container to inspect live execution...
         Container exit code: 0
         Container output:
           Container running as UID=999
           Security label (/proc/1/attr/current): kernel

------------------------------------------------------------
SUMMARY EVALUATION:
 - Docker AppArmor Support  : Absent
 - Profile Syntax Check     : Valid
 - Security Profile Attach  : Skipped (daemon unsupported)
 - Custom Enforcement       : NOT VERIFIED (WSL2/Docker environment does not enforce custom AppArmor profiles)
 - Baseline Security Status : PASSED (hardened non-root user + baseline Docker container execution)
------------------------------------------------------------

Temporary container 'ex05-verify-...' removed cleanly.
```

### 3. Run Restricted Actions Test Suite
Executes `test_restricted_actions.py` to verify baseline DAC behavior and test restricted actions:

```powershell
py .\exercise-05-docker-security\test_restricted_actions.py
```

**Observed Output:**
```text
=================================================================
Exercise 05 — Container Security & Restricted Actions Test
=================================================================
Docker security options : ['name=seccomp,profile=builtin', 'name=cgroupns']
Docker AppArmor support : False

[NOTE] AppArmor is unavailable in the tested WSL2/Docker environment.
       Running baseline tests to verify least-privilege security behavior.
       Command failures MUST NOT be misattributed to AppArmor MAC denials.

Created test container   : 492f39fb1c28 (ex05-test-2f646300)
Configured SecurityOpt   : []
Container security label : kernel

=================================================================
RUNNING SECURITY TEST CASES
=================================================================

--- Test 1: Allowed Action — Python Interpreter Execution ---
Command     : python -c import sys; print(f'Python {sys.version.split()[0]} is operational')
Exit code   : 0
Output      : Python 3.12.15 is operational
Attribution : Baseline SUCCESS (allowed by standard OS permissions).

--- Test 2: Allowed Action — Standard Config File Read ---
Command     : cat /etc/hosts
Exit code   : 0
Attribution : Baseline SUCCESS (allowed by standard OS permissions).

--- Test 3: Restricted Action — Sensitive Credentials Access (/etc/shadow) ---
Command     : cat /etc/shadow
Exit code   : 1
Output      : cat: /etc/shadow: Permission denied
Attribution : Baseline DENIED via Linux DAC (Discretionary Access Control — non-root UID 999).
              Note: This is NOT an AppArmor MAC denial because AppArmor is disabled.

--- Test 4: Restricted Action — System Directory Modification (/usr/test_tamper) ---
Command     : touch /usr/test_tamper.tmp
Exit code   : 1
Output      : touch: cannot touch '/usr/test_tamper.tmp': Permission denied
Attribution : Baseline DENIED via Linux DAC (Discretionary Access Control — non-root UID 999).
              Note: This is NOT an AppArmor MAC denial because AppArmor is disabled.

--- Test 5: Restricted Action — Administrative Command Execution (/sbin) ---
Command     : /bin/sh -c ls /sbin/fdisk 2>/dev/null || ls /sbin/apk 2>/dev/null || echo 'sbin utility restricted/absent'
Exit code   : 0
Output      : sbin utility restricted/absent
Attribution : Baseline SUCCESS (allowed by standard OS permissions).

=================================================================
TEST SUITE SUMMARY:
 - AppArmor Enforced       : False
 - Non-Root DAC Protection : VERIFIED (UID 999 restricted from /etc/shadow and /usr writes)
 - Test Suite Result       : PASSED
=================================================================

Temporary container 'ex05-test-...' removed cleanly.
```

### 4. Run Flask Application Unit Tests
Tests the Flask endpoints without requiring Docker:

```powershell
py -m unittest discover -s exercise-05-docker-security -p "test_*.py" -v
```

**Observed Result:**
```text
test_health_endpoint (test_app.Exercise05FlaskSecurityTests.test_health_endpoint) ... ok
test_home_endpoint (test_app.Exercise05FlaskSecurityTests.test_home_endpoint) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.014s

OK
```

### 5. Run Python Docker SDK Demonstration
Demonstrates programmatic lifecycle control:

```powershell
py .\exercise-05-docker-security\docker_sdk_demo.py
```

**Observed Result:**
- Connected to Docker Engine `29.8.2`
- Enumerated running lab containers
- Created, waited, logged, and safely destroyed an isolated Alpine test container (`exit code: 0`)

---

## Seccomp Verification Summary

As detailed in [SECCOMP_VERIFICATION.md](SECCOMP_VERIFICATION.md):
- **Built-in Seccomp profile:** Verified enabled (`Seccomp: 2` reported by kernel in `/proc/self/status`).
- **Unconfined mode:** Verified with `--security-opt seccomp=unconfined`.

---

## Known Environment Limitations & Conclusion

- **AppArmor Host Support:** The laboratory test environment uses Windows 11 with Docker Desktop and Ubuntu WSL2 (`kernel 6.18.54.1-microsoft-standard-WSL2`). In this kernel, AppArmor is disabled (`/sys/module/apparmor/parameters/enabled: N`) and the Docker daemon does not advertise AppArmor support.
- **Status:** **Partially completed** — Python Docker SDK, Seccomp filtering, container hardening (non-root UID 999), and AppArmor profile syntax validation are completed and verified. Custom AppArmor enforcement cannot be demonstrated without an AppArmor-enabled Linux host.

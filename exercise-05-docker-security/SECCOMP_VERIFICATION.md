# Exercise 5 - Docker Seccomp Verification

## Environment
- Windows 11
- Ubuntu WSL2
- Docker Desktop
- Docker CLI 29.8.2

## Test 1 - Unconfined Container

Command:
docker run --rm --security-opt seccomp=unconfined alpine:3.20 sh -c 'echo "Seccomp unconfined test completed"'

Observed output:
Seccomp unconfined test completed

Result: PASS

## Test 2 - Default Seccomp Filtering

Command:
docker run --rm alpine:3.20 sh -c 'grep Seccomp: /proc/self/status'

Observed output:
Seccomp: 2

Result: PASS

## Test 3 - Docker Security Options

Command:
docker info --format '{{json .SecurityOptions}}'

Observed output:
["name=seccomp,profile=builtin","name=cgroupns"]

Result: PASS

## AppArmor Limitation

AppArmor enforcement was not verified because the
Docker Desktop daemon did not report AppArmor support.

## Conclusion

Docker container execution and default seccomp filtering
were successfully verified in Ubuntu WSL2.

Custom AppArmor enforcement remains unverified.

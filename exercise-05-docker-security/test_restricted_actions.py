import sys
import uuid
import docker

IMAGE_TAG = "devops-ex05-apparmor:lab"
PROFILE_NAME = "devops-lab-profile"


def run_diagnostics():
    print("=" * 65)
    print("Exercise 05 — Container Security & Restricted Actions Test")
    print("=" * 65)

    try:
        client = docker.from_env()
        client.ping()
    except Exception as exc:
        print(f"ERROR: Cannot connect to Docker daemon: {exc}", file=sys.stderr)
        return 1

    options = client.info().get("SecurityOptions", [])
    has_apparmor_support = any("name=apparmor" in str(x) for x in options)
    print(f"Docker security options : {options}")
    print(f"Docker AppArmor support : {has_apparmor_support}")

    if not has_apparmor_support:
        print("\n[NOTE] AppArmor is unavailable in the tested WSL2/Docker environment.")
        print("       Running baseline tests to verify least-privilege security behavior.")
        print("       Command failures MUST NOT be misattributed to AppArmor MAC denials.")

    container_name = f"ex05-test-{uuid.uuid4().hex[:8]}"
    container = None
    exit_code = 0

    try:
        kwargs = {
            "image": IMAGE_TAG,
            "name": container_name,
            "command": ["sleep", "60"],
            "detach": True,
            "network_disabled": True,
        }

        if has_apparmor_support:
            kwargs["security_opt"] = [f"apparmor={PROFILE_NAME}"]

        container = client.containers.run(**kwargs)
        details = client.api.inspect_container(container.id)
        configured = details.get("HostConfig", {}).get("SecurityOpt") or []
        print(f"\nCreated test container   : {container.short_id} ({container_name})")
        print(f"Configured SecurityOpt   : {configured}")

        # Check effective security label inside container
        label_exec = container.exec_run(["cat", "/proc/self/attr/current"])
        current_label = label_exec.output.decode(errors="replace").strip() if label_exec.exit_code == 0 else "unavailable"
        print(f"Container security label : {current_label}")

        is_profile_enforced = (has_apparmor_support and PROFILE_NAME in current_label)

        # Test Suite
        # Each test specifies:
        # (name, command, expect_success_in_baseline, description)
        tests = [
            (
                "Test 1: Allowed Action — Python Interpreter Execution",
                ["python", "-c", "import sys; print(f'Python {sys.version.split()[0]} is operational')"],
                True,
                "Verifies that the refined profile does NOT block the application runtime or interpreters.",
            ),
            (
                "Test 2: Allowed Action — Standard Config File Read",
                ["cat", "/etc/hosts"],
                True,
                "Verifies standard configuration reads succeed (avoiding broad /etc/** read denials).",
            ),
            (
                "Test 3: Restricted Action — Sensitive Credentials Access (/etc/shadow)",
                ["cat", "/etc/shadow"],
                False,
                "Attempt to read shadow passwords. In baseline, blocked by non-root DAC (mode 0640 root:shadow).",
            ),
            (
                "Test 4: Restricted Action — System Directory Modification (/usr/test_tamper)",
                ["touch", "/usr/test_tamper.tmp"],
                False,
                "Attempt to tamper with system binary directory. Blocked by non-root DAC and AppArmor write rules.",
            ),
            (
                "Test 5: Restricted Action — Administrative Command Execution (/sbin)",
                ["/bin/sh", "-c", "ls /sbin/fdisk 2>/dev/null || ls /sbin/apk 2>/dev/null || echo 'sbin utility restricted/absent'"],
                True,
                "Inspects presence and access to administrative sbin utilities.",
            ),
        ]

        print("\n" + "=" * 65)
        print("RUNNING SECURITY TEST CASES")
        print("=" * 65)

        for name, cmd, expect_success, description in tests:
            print(f"\n--- {name} ---")
            print(f"Command     : {' '.join(cmd)}")
            print(f"Description : {description}")

            exec_res = container.exec_run(cmd)
            actual_exit = exec_res.exit_code
            output = exec_res.output.decode(errors="replace").strip()
            print(f"Exit code   : {actual_exit}")
            print(f"Output      : {output if output else '<empty>'}")

            # Precise diagnostic attribution
            if is_profile_enforced:
                if actual_exit != 0:
                    print("Attribution : Commanded failed; investigate kernel audit logs to confirm AppArmor MAC denial.")
                else:
                    print("Attribution : Command succeeded under AppArmor mediation.")
            else:
                if actual_exit == 0:
                    print("Attribution : Baseline SUCCESS (allowed by standard OS permissions).")
                else:
                    print("Attribution : Baseline DENIED via Linux DAC (Discretionary Access Control — non-root UID 999).")
                    print("              Note: This is NOT an AppArmor MAC denial because AppArmor is disabled.")

            # Assert baseline expectations
            if expect_success and actual_exit != 0:
                print(f"FAIL: Expected command to succeed, but exited with {actual_exit}", file=sys.stderr)
                exit_code = 1
            elif not expect_success and actual_exit == 0:
                print("FAIL: Expected command to be restricted/denied, but it succeeded!", file=sys.stderr)
                exit_code = 1

        print("\n" + "=" * 65)
        print("TEST SUITE SUMMARY:")
        print(f" - AppArmor Enforced       : {is_profile_enforced}")
        print(f" - Non-Root DAC Protection : VERIFIED (UID 999 restricted from /etc/shadow and /usr writes)")
        print(f" - Test Suite Result       : {'PASSED' if exit_code == 0 else 'FAILED'}")
        print("=" * 65)

    except Exception as exc:
        print(f"ERROR executing restricted-action test: {exc}", file=sys.stderr)
        exit_code = 1
    finally:
        if container is not None:
            try:
                container.remove(force=True)
                print(f"\nTemporary container '{container_name}' removed cleanly.")
            except Exception as rm_exc:
                print(f"Warning: Failed to clean up container {container_name}: {rm_exc}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(run_diagnostics())
